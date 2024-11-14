from typing import List

from icosa.api import (
    COMMON_ROUTER_SETTINGS,
    POLY_CATEGORY_MAP,
    AssetPagination,
    build_format_q,
)
from icosa.models import PRIVATE, PUBLIC, UNLISTED, Asset, Tag
from icosa.models import User as IcosaUser
from ninja import Query, Router
from ninja.errors import HttpError
from ninja.pagination import paginate

from django.db.models import Q

from .authentication import AuthBearer
from .schema import (
    AssetFilters,
    AssetSchemaOut,
    FullUserSchema,
    PatchUserSchema,
    UserAssetFilters,
    get_keyword_q,
)

router = Router()


@router.get(
    "/me",
    auth=AuthBearer(),
    response=FullUserSchema,
)
def get_users_me(request):
    return IcosaUser.from_ninja_request(request)


@router.patch(
    "/me",
    auth=AuthBearer(),
    response=FullUserSchema,
)
def update_user(
    request,
    patch_user: PatchUserSchema,
):
    current_user = IcosaUser.from_ninja_request(request)
    url = getattr(patch_user, "url", "").strip() or current_user.url

    if (
        IcosaUser.objects.filter(url__iexact=url).count() != 0
        and url != current_user.url
    ):
        # Used to return 403. James believes this is the wrong status code.
        # Better to use Unprocessable Entity.
        raise HttpError(422, "This URL is already in use")
    for key, value in patch_user.__dict__.items():
        if getattr(patch_user, key, None) is not None:
            setattr(current_user, key, value)
    current_user.save()
    return current_user


@router.get(
    "/me/assets",
    auth=AuthBearer(),
    response=List[AssetSchemaOut],
    **COMMON_ROUTER_SETTINGS,
)
@paginate(AssetPagination)
def get_me_assets(
    request,
    filters: UserAssetFilters = Query(...),
):
    owner = IcosaUser.from_ninja_request(request)
    q = Q(
        owner=owner,
    )
    ex_q = Q()
    if filters.visibility:
        if filters.visibility in [
            PRIVATE,
            UNLISTED,
        ]:
            q &= Q(visibility=filters.visibility)
        elif filters.visibility == "PUBLISHED":
            q &= Q(visibility=PUBLIC)
        else:
            raise HttpError(
                400,
                "Unknown visibility specifier. Expected one of PUBLISHED, PRIVATE, UNLISTED.",  # TODO: brittle
            )

    if filters.format:
        q &= build_format_q(filters.format)

    if filters.tag:
        tags = Tag.objects.filter(name__in=filters.tag)
        q &= Q(tags__in=tags)
    if filters.category:
        category_str = filters.category.upper()
        category_str = POLY_CATEGORY_MAP.get(category_str, category_str)
        q &= Q(category__iexact=category_str)
    if filters.curated:
        q &= Q(curated=True)
    if filters.name:
        q &= Q(name__icontains=filters.name)
    if filters.description:
        q &= Q(description__icontains=filters.description)
    try:
        keyword_q = get_keyword_q(filters)
    except HttpError:
        raise
    # TODO: orderBy
    assets = Asset.objects.filter(q, keyword_q).exclude(ex_q).distinct()
    return assets


@router.get(
    "/me/likedassets",
    auth=AuthBearer(),
    response=List[AssetSchemaOut],
    **COMMON_ROUTER_SETTINGS,
)
@paginate(AssetPagination)
def get_me_likedassets(
    request,
    filters: AssetFilters = Query(...),
):
    owner = IcosaUser.from_ninja_request(request)
    liked_assets = owner.likedassets.all()
    q = Q(
        visibility__in=[PUBLIC, UNLISTED],
    )
    q |= Q(visibility__in=[PRIVATE, UNLISTED], owner=owner)

    if filters.format:
        q &= build_format_q(filters.format)

    if filters.orderBy and filters.orderBy == "LIKED_TIME":
        liked_assets = liked_assets.order_by("-date_liked")

    # Get the ordered IDs for sorting later, if we need to. We can't use
    # `owner.likes.all` because we need the timestamp of when the asset was
    # liked.
    liked_ids = list(liked_assets.values_list("asset__pk", flat=True))
    q &= Q(pk__in=liked_ids)

    if filters.tag:
        tags = Tag.objects.filter(name__in=filters.tag)
        q &= Q(tags__in=tags)
    if filters.category:
        category_str = filters.category.upper()
        category_str = POLY_CATEGORY_MAP.get(category_str, category_str)
        q &= Q(category__iexact=category_str)
    if filters.curated:
        q &= Q(curated=True)
    if filters.name:
        q &= Q(name__icontains=filters.name)
    if filters.description:
        q &= Q(description__icontains=filters.description)
    author_name = filters.authorName or filters.author_name or None
    if author_name is not None:
        q &= Q(owner__displayname__icontains=author_name)
    # TODO: orderBy
    try:
        keyword_q = get_keyword_q(filters)
        q &= keyword_q
    except HttpError:
        raise

    assets = Asset.objects.filter(q)

    if filters.orderBy:
        if filters.orderBy == "LIKED_TIME":
            # Sort the assets by order of liked ID. Slow, but
            # database-agnostic. Postgres and MySql have different ways to do
            # this, and we'd need to use the `extra` params in our query, which
            # are database-specific.
            assets = sorted(assets, key=lambda i: liked_ids.index(i.pk))
        elif filters.orderBy == "NEWEST":
            assets = assets.order_by("-create_time")
        elif filters.orderBy == "OLDEST":
            assets = assets.order_by("create_time")
        elif filters.orderBy == "BEST":
            assets = assets.order_by("-rank")
        else:
            pass
    return assets
