import logging
import json

from logging import Logger
from typing import Optional

from services.switcher_store import SwitcherInstallationStoreService

from slack_sdk.oauth.installation_store.installation_store import InstallationStore
from slack_sdk.oauth.installation_store.models.bot import Bot
from slack_sdk.oauth.installation_store.models.installation import Installation
from slack_sdk.oauth.installation_store.async_installation_store import (
    AsyncInstallationStore,
)

class SwitcherAppInstallationStore(InstallationStore, AsyncInstallationStore):
    def __init__(self, *, logger: Logger = logging.getLogger(__name__)):
        self._logger = logger
        self._store_service = SwitcherInstallationStoreService()

    @property
    def logger(self) -> Logger:
        if self._logger is None:
            self._logger = logging.getLogger(__name__)
        return self._logger

    async def async_save(self, installation: Installation):
        return self.save(installation)

    def save(self, installation: Installation):
        e_id = installation.enterprise_id
        t_id = installation.team_id
        u_id = installation.user_id

        try:
            self._store_service.save_installation(
                enterprise_id = e_id,
                team_id = t_id,
                user_id = u_id,
                installation_payload = installation.__dict__,
                bot_payload = installation.to_bot().__dict__
            )
        except Exception as e:
            message = \
                "Failed to save installation data for enterprise:" \
                f"{e_id}, team: {t_id}: {e}"
                
            self.logger.warning(message)

    async def async_find_bot(
        self,
        *,
        enterprise_id: Optional[str],
        team_id: Optional[str],
        is_enterprise_install: Optional[bool] = False,
    ) -> Optional[Bot]:
        return self.find_bot(
            enterprise_id = enterprise_id,
            team_id = team_id,
            is_enterprise_install = is_enterprise_install,
        )

    def find_bot(
        self,
        *,
        enterprise_id: Optional[str],
        team_id: Optional[str],
        is_enterprise_install: Optional[bool] = False,
    ) -> Optional[Bot]:
        try:
            response = self._store_service.find_bot(
                enterprise_id = enterprise_id,
                team_id = team_id
            )
            
            bot_payload = json.loads(response.data)
            return Bot(**bot_payload)
        except Exception as e:
            message = \
                "Failed to find bot installation data for enterprise:" \
                f"{enterprise_id}, team: {team_id}: {e}"
            
            self.logger.warning(message)
            return None

    async def async_find_installation(
        self,
        *,
        enterprise_id: Optional[str],
        team_id: Optional[str],
        user_id: Optional[str] = None,
        is_enterprise_install: Optional[bool] = False,
    ) -> Optional[Installation]:
        return self.find_installation(
            enterprise_id = enterprise_id,
            team_id = team_id,
            user_id = user_id,
            is_enterprise_install = is_enterprise_install,
        )

    def find_installation(
        self,
        *,
        enterprise_id: Optional[str],
        team_id: Optional[str],
        user_id: Optional[str] = None,
        is_enterprise_install: Optional[bool] = False,
    ) -> Optional[Installation]:
        try:
            response = self._store_service.find_installation(
                enterprise_id = enterprise_id,
                team_id = team_id
            )

            installation_payload = json.loads(response.data)
            return Installation(**installation_payload)
        except Exception as e:
            message = \
                "Failed to find an installation data for enterprise:" \
                f"{enterprise_id}, team: {team_id}: {e}"
            
            self.logger.warning(message)
            return None

    async def async_delete_bot(
        self, *, enterprise_id: Optional[str], team_id: Optional[str]
    ) -> None:
        return self.delete_bot(enterprise_id = enterprise_id, team_id = team_id)

    def delete_bot(
        self, 
        *, 
        enterprise_id: Optional[str], 
        team_id: Optional[str]
    ) -> None:
        self._store_service.delete_bot(
            enterprise_id = enterprise_id,
            team_id = team_id
        )

    async def async_delete_installation(
        self,
        *,
        enterprise_id: Optional[str],
        team_id: Optional[str],
        user_id: Optional[str] = None,
    ) -> None:
        return self.delete_installation(
            enterprise_id = enterprise_id, team_id = team_id, user_id = user_id
        )

    def delete_installation(
        self,
        *,
        enterprise_id: Optional[str],
        team_id: Optional[str],
        user_id: Optional[str] = None,
    ) -> None:
        try:
            self._store_service.delete_installation(
                enterprise_id = enterprise_id,
                team_id = team_id,
                user_id = user_id 
            )
        except Exception as e:
            message = \
                "Failed to delete installation data for enterprise:" \
                f"{enterprise_id}, team: {team_id}: {e}"
            
            self.logger.warning(message)