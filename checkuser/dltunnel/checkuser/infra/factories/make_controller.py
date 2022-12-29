from checkuser.infra.controller import Controller
from checkuser.infra.controllers.check_user import CheckUserController
from checkuser.infra.controllers.kill_connection import KillConnectionController
from checkuser.infra.controllers.all_connections import AllConnectionsController

from checkuser.data.executor import CommandExecutorImpl
from checkuser.data.driver import DriverImpl, FormatDateUS
from checkuser.data.repository import UserRepositoryImpl, InMemoryUserRepository
from checkuser.domain.use_case import CheckUserUseCase, KillConnectionUseCase, AllConnectionsUseCase
from checkuser.data.connection import (
    AUXOpenVPNConnection,
    SSHConnection,
    OpenVPNConnection,
    V2rayConnection,
    V2RayService,
)


def make_controller() -> CheckUserController:
    repository = UserRepositoryImpl(
        DriverImpl(
            CommandExecutorImpl(),
            FormatDateUS(),
        ),
    )

    return CheckUserController(
        CheckUserUseCase(
            repository,
            [
                SSHConnection(CommandExecutorImpl()),
                OpenVPNConnection(AUXOpenVPNConnection()),
                V2rayConnection(V2RayService(CommandExecutorImpl())),
            ],
        )
    )


def make_kill_controller() -> KillConnectionController:
    return KillConnectionController(
        KillConnectionUseCase(
            [
                SSHConnection(CommandExecutorImpl()),
                OpenVPNConnection(AUXOpenVPNConnection()),
            ]
        )
    )


def make_all_controller() -> AllConnectionsController:
    return AllConnectionsController(
        AllConnectionsUseCase(
            [
                SSHConnection(CommandExecutorImpl()),
                OpenVPNConnection(AUXOpenVPNConnection()),
                V2rayConnection(V2RayService(CommandExecutorImpl())),
            ]
        )
    )


class Controllers:
    _controllers = {
        'check': make_controller(),
        'kill': make_kill_controller(),
        'all': make_all_controller(),
    }

    @staticmethod
    def get(controller: str) -> Controller:
        return Controllers._controllers[controller]
