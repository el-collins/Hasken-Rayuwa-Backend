from models.blogs import Blog


class BlogDataMultiUpdate(BaseModel):
    updates: Dict[str, Union[str, int, Blog]]