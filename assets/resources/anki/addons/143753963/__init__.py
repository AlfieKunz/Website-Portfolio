# Copyright (C) lovac42 2021 <https://github.com/lovac42> SpellingPolice <https://github.com/lovac42/SpellingPolice>
# Copyright (C) Valentin 2023 <https://github.com/ValentinSchmitz> Spell Checker <https://github.com/ValentinSchmitz/spell-checker>
# Copyright (C) Shigeyuki 2025 <http://patreon.com/Shigeyuki>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from .main import setup_hooks
from .shige_config.popup_config import set_gui_hook_change_log

setup_hooks()
set_gui_hook_change_log()