# Mycroft Server - Backend
# Copyright (C) 2019 Mycroft AI Inc
# SPDX-License-Identifier: 	AGPL-3.0-or-later
#
# This file is part of the Mycroft Server.
#
# The Mycroft Server is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""
Logic that uses the Github REST API to extract repository-related metadata
"""
from logging import getLogger
from urllib.request import urlopen

from github import Github

_log = getLogger(__package__)


def log_into_github(user_name: str, user_password: str) -> Github:
    _log.info('logging into GitHub as "{}"'.format(user_name))
    return Github(user_name, user_password)


def download_repository_file(github, repository_name, branch, file_path):
    organization = github.get_organization('MycroftAI')
    repository = organization.get_repo(repository_name)
    repository_contents = repository.get_contents(file_path, ref=branch)

    with urlopen(repository_contents.download_url) as repository_file:
        return repository_file.read()
