class AppConfig:
    APP_TITLE = "Personal Assistance"
    
    @classmethod
    def get_app_title(cls):
        return cls.APP_TITLE
    
    @classmethod
    def set_app_title(cls, title):
        cls.APP_TITLE = title