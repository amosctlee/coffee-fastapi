
from functools import lru_cache
from . import config


# 每次呼叫都回傳相同value，不用重新讀檔
@lru_cache()
def get_settings():
    # 把settings 放在 dependency 中，可以很方便覆寫 value，測試時尤其有用
    # 以下為覆寫 dependency 的方式
    # def get_settings_override():
    #     return Settings(admin_email="testing_admin@example.com")
    # app.dependency_overrides[get_settings] = get_settings_override

    return config.Settings()



# Dependency
def get_db():
    from .database import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

