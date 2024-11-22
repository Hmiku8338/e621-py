from __future__ import annotations

import itertools
from typing import TYPE_CHECKING, Any, Iterable, List, Optional, Set, Union

from backports.cached_property import cached_property
from pydantic import Field
from typing_extensions import Protocol

from .base_model import BaseModel

if TYPE_CHECKING:
    from .api import E621


class File(BaseModel):
    width: Optional[int]
    height: Optional[int]
    ext: str
    size: Optional[int]
    md5: Optional[str]
    url: Optional[str]


class Preview(BaseModel):
    width: int
    height: int
    url: Optional[str]


class Field720p(BaseModel):
    type: str
    height: int
    width: int
    urls: List[Optional[str]]


class Field480p(Field720p):
    pass


class Original(BaseModel):
    type: str
    height: int
    width: int
    urls: List[Optional[str]]


class Alternates(BaseModel):
    field_720p: Optional[Field720p] = Field(None, alias="720p")
    field_480p: Optional[Field480p] = Field(None, alias="480p")
    original: Optional[Original] = None


class Sample(BaseModel):
    has: bool
    height: int
    width: int
    url: Optional[str]
    alternates: Alternates


class Score(BaseModel):
    up: int
    down: int
    total: int


class Tags(BaseModel):
    general: List[str]
    species: List[str]
    character: List[str]
    copyright: List[str]
    artist: List[str]
    invalid: List[str]
    lore: List[str]
    meta: List[str]


class Flags(BaseModel):
    pending: bool
    flagged: bool
    note_locked: bool
    status_locked: bool
    rating_locked: bool
    deleted: bool


class Relationships(BaseModel):
    parent_id: Optional[int]
    has_children: bool
    has_active_children: bool
    children: List[int]


class Posts(BaseModel):
    posts: List[Post]


class PostFlag(BaseModel):
    id: int
    created_at: str
    post_id: int
    reason: str
    is_resolved: bool
    updated_at: Optional[str]
    is_deletion: bool
    category: str
    creator_id: Optional[int] = None


class Tag(BaseModel):
    id: int
    name: str
    post_count: int
    related_tags: str
    related_tags_updated_at: Optional[str]
    category: int
    is_locked: bool
    created_at: str
    updated_at: Optional[str]


class TagAlias(BaseModel):
    id: int
    antecedent_name: str
    reason: str
    creator_id: int
    created_at: Optional[str] = None
    forum_post_id: Optional[int]
    updated_at: Optional[str]
    forum_topic_id: Optional[int]
    consequent_name: str
    status: str
    post_count: int
    approver_id: Optional[int]


class Note(BaseModel):
    id: int
    created_at: str
    updated_at: Optional[str]
    creator_id: int
    x: int
    y: int
    width: int
    height: int
    version: int
    is_active: bool
    post_id: int
    body: str
    creator_name: str


class User(BaseModel):
    id: int
    created_at: str
    name: str
    level: int
    base_upload_limit: int
    post_upload_count: int
    post_update_count: int
    note_update_count: int
    is_banned: bool
    can_approve_posts: bool
    can_upload_free: bool
    level_string: str
    avatar_id: Optional[int]


class PostVersion(BaseModel):
    id: int
    post_id: int
    tags: str
    updater_id: int
    updated_at: Optional[str]
    rating: str
    parent_id: Optional[int]
    source: str
    description: str
    reason: Optional[str]
    locked_tags: Optional[str]
    added_tags: List[str]
    removed_tags: List[str]
    added_locked_tags: List[str]
    removed_locked_tags: List[str]
    rating_changed: bool
    parent_changed: bool
    source_changed: bool
    description_changed: bool
    version: int
    obsolete_added_tags: str
    obsolete_removed_tags: str
    unchanged_tags: str
    updater_name: str


class PostApproval(BaseModel):
    id: int
    user_id: int
    post_id: int
    created_at: str
    updated_at: Optional[str]


class NoteVersion(BaseModel):
    id: int
    created_at: str
    updated_at: Optional[str]
    x: int
    y: int
    width: int
    height: int
    body: str
    version: int
    is_active: bool
    note_id: int
    post_id: int
    updater_id: int


class WikiPage(BaseModel):
    id: int
    created_at: str
    updated_at: Optional[str]
    title: str
    body: str
    creator_id: int
    is_locked: bool
    updater_id: int
    is_deleted: bool
    other_names: List[str]
    creator_name: str
    category_name: Optional[int] = None


class WikiPageVersion(BaseModel):
    id: int
    created_at: str
    updated_at: Optional[str]
    title: str
    body: str
    updater_id: int
    wiki_page_id: int
    is_locked: bool
    other_names: List[str]
    is_deleted: bool
    reason: Optional[str]


class Url(BaseModel):
    id: int
    artist_id: int
    url: str
    normalized_url: str
    created_at: str
    updated_at: Optional[str]
    is_active: bool


class Artist(BaseModel):
    id: int
    name: str
    updated_at: Optional[str]
    is_active: bool
    other_names: List[str]
    group_name: str
    linked_user_id: Optional[int]
    created_at: str
    creator_id: int
    is_locked: bool
    notes: Optional[str]
    urls: List[Url]


class ArtistVersion(BaseModel):
    id: int
    artist_id: int
    name: str
    updater_id: int
    created_at: str
    updated_at: Optional[str]
    is_active: bool
    other_names: List[str]
    group_name: str
    is_banned: bool
    notes_changed: bool
    urls: List[str]


class TagTypeVersion(BaseModel):
    id: int
    created_at: str
    updated_at: Optional[str]
    old_type: int
    new_type: int
    is_locked: bool
    tag_id: int
    creator_id: int


class TagImplication(BaseModel):
    id: int
    reason: str
    creator_id: int
    created_at: str
    forum_post_id: int
    antecedent_name: str
    consequent_name: str
    status: str
    forum_topic_id: int
    updated_at: Optional[str]
    descendant_names: List[str]
    approver_id: Optional[int]


class BulkUpdateRequest(BaseModel):
    id: int
    user_id: int
    forum_topic_id: int
    script: str
    status: str
    created_at: str
    updated_at: Optional[str]
    approver_id: Optional[int]
    forum_post_id: Optional[int]
    title: str


class Blip(BaseModel):
    id: int
    creator_id: int
    body: str
    response_to: Optional[int]
    created_at: str
    updated_at: Optional[str]
    is_hidden: bool
    warning_type: Any
    warning_user_id: Optional[int]
    creator_name: str


class Takedown(BaseModel):
    id: int
    status: str
    approver_id: Optional[int]
    reason_hidden: bool
    created_at: str
    updated_at: Optional[str]
    post_count: int


class UserFeedback(BaseModel):
    id: int
    user_id: int
    creator_id: int
    created_at: str
    body: str
    category: str
    updated_at: Optional[str]


class ForumTopic(BaseModel):
    id: int
    creator_id: int
    updater_id: int
    title: str
    response_count: int
    is_sticky: bool
    is_locked: bool
    is_hidden: bool
    created_at: str
    updated_at: Optional[str]
    category_id: int
    min_level: int


class ForumPost(BaseModel):
    id: int
    created_at: str
    updated_at: Optional[str]
    body: str
    creator_id: int
    updater_id: int
    topic_id: int
    is_hidden: bool
    warning_type: Any
    warning_user_id: Optional[int]


class PostSet(BaseModel):
    id: int
    created_at: str
    updated_at: Optional[str]
    creator_id: int
    is_public: bool
    name: str
    shortname: str
    description: str
    post_count: int
    transfer_on_delete: bool
    post_ids: List[int]


class Post(BaseModel):
    id: int
    created_at: str
    updated_at: Optional[str]
    file_obj: Optional[File] = Field(default=None, alias="file")
    file_url: Optional[str] = None
    large_file_url: Optional[str] = None
    preview_file_url: Optional[str] = None
    file_ext: Optional[str] = None
    file_size: Optional[int] = None
    preview: Optional[Preview]
    sample: Optional[Sample]
    score: Union[Score, None, str]
    tags: Optional[Tags]
    locked_tags: Optional[List[str]]
    tag_string_general: Optional[str] = None
    tag_string_character: Optional[str] = None
    tag_string_copyright: Optional[str] = None
    tag_string_artist: Optional[str] = None
    tag_string_meta: Optional[str] = None
    change_seq: Optional[int]
    flags: Optional[Flags]
    rating: str
    fav_count: Optional[int]
    sources: Optional[List[str]]
    pools: Optional[List[int]]
    relationships: Optional[Relationships]
    approver_id: Optional[int]
    uploader_id: int
    description: Optional[str]
    comment_count: Optional[int]
    is_favorited: Optional[bool]
    has_notes: Optional[bool]
    duration: Optional[float]

    @cached_property
    def all_tags(self) -> Set[str]:
        if self.tags is not None:
            return set(
                self.tags.general
                + self.tags.species
                + self.tags.character
                + self.tags.copyright
                + self.tags.artist
                + self.tags.invalid
                + self.tags.lore
                + self.tags.meta
            )
        return set(
            itertools.chain.from_iterable(
                {
                    getattr(self, field, "").split()
                    for field in (
                        "tag_string_general",
                        "tag_string_character",
                        "tag_string_copyright",
                        "tag_string_artist",
                        "tag_string_meta",
                    )
                }
            )
        )

    @cached_property
    def file(self) -> Optional[File]:
        if self.file_obj is not None:
            return self.file_obj
        elif self.large_file_url is not None:
            url = self.large_file_url
            ext = self.large_file_url.rsplit(".", 1)[-1]
        elif self.file_url is not None:
            url = self.file_url
            ext = self.file_ext.strip(".") if self.file_ext else None
        else:
            return None

        if ext:
            return File(
                e621api=self.e621api,
                size=self.file_size,
                width=None,
                height=None,
                ext=ext,
                md5=None,
                url=url,
            )


class _HasPostIdsAndE621API(Protocol):
    e621api: "E621"
    post_ids: List[int]


class _PostsGetterMixin:
    @cached_property
    def posts(self: _HasPostIdsAndE621API) -> List[Post]:
        return self.e621api.posts.search(tags=f"id:{','.join(map(str, self.post_ids))}")


class Pool(BaseModel, _PostsGetterMixin):
    id: int
    name: str
    created_at: str
    updated_at: Optional[str]
    creator_id: int
    description: str
    is_active: Optional[bool]
    category: str
    is_deleted: Optional[bool] = None
    post_ids: List[int]
    creator_name: str
    post_count: int


class EnrichedPostSet(PostSet, _PostsGetterMixin):
    pass


class BlackList(Set[str]):
    def intersects(self, iterable: Iterable[str]) -> bool:
        for val in self:
            if " " in val and all(v in iterable for v in val.replace("  ", " ").split(" ")):
                return True
            elif val in iterable:
                return True
        return False


class AuthenticatedUser(User):
    wiki_page_version_count: int
    artist_version_count: int
    pool_version_count: int
    forum_post_count: int
    comment_count: int
    flag_count: int
    positive_feedback_count: int
    neutral_feedback_count: int
    negative_feedback_count: int
    upload_limit: int
    show_avatars: Optional[bool] = None
    blacklist_avatars: Optional[bool] = None
    blacklist_users: bool
    description_collapsed_initially: bool
    hide_comments: bool
    show_hidden_comments: bool
    show_post_statistics: bool
    has_mail: bool
    receive_email_notifications: bool
    enable_keyboard_navigation: bool
    enable_privacy_mode: bool
    style_usernames: bool
    enable_auto_complete: bool
    has_saved_searches: Optional[bool] = None
    disable_cropped_thumbnails: bool
    disable_mobile_gestures: Optional[bool] = None
    enable_safe_mode: bool
    disable_responsive_mode: bool
    disable_post_tooltips: Optional[bool] = None
    no_flagging: bool
    no_feedback: Optional[bool] = None
    disable_user_dmails: bool
    enable_compact_uploader: bool
    replacements_beta: bool
    updated_at: str
    email: str
    last_logged_in_at: str
    last_forum_read_at: str
    recent_tags: str
    comment_threshold: int
    default_image_size: str
    favorite_tags: str
    blacklisted_tags: str
    time_zone: str
    per_page: int
    custom_style: str
    favorite_count: int
    api_regen_multiplier: int
    api_burst_limit: int
    remaining_api_limit: int
    statement_timeout: int
    favorite_limit: int
    tag_query_limit: int

    @cached_property
    def blacklist(self) -> BlackList:
        return BlackList(self.blacklisted_tags.split("\n"))
