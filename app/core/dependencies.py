# app/core/dependencies.py

from typing import Annotated

from fastapi import Depends

from app.core.config import Settings, get_settings

# Annotated shortcut for injecting Settings
SettingsDep = Annotated[Settings, Depends(get_settings)]
