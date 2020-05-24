class Video():
    def __init__(self, 
        video_id, 
        trending_date, 
        title, 
        channel_title, 
        category_id, 
        publish_time, 
        tags, 
        views, 
        likes, 
        dislikes, 
        comment_count, 
        thumbnail_link, 
        comments_disabled, 
        ratings_disabled, 
        video_error_or_removed, 
        description ):

        self.video_id = video_id
        self.trending_date = trending_date
        self.title = title
        self.channel_title = channel_title
        self.category_id = category_id
        self.publish_time = publish_time
        self.tags = tags
        self.views = views
        self.likes = likes
        self.dislikes = dislikes
        self.comment_count = comment_count
        self.thumbnail_link = thumbnail_link
        self.comments_disabled = comments_disabled
        self.ratings_disabled = ratings_disabled
        self.video_error_or_removed = video_error_or_removed
        self.description = description
