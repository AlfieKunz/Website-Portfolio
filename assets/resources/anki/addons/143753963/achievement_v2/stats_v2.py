# Anki Leaderboard
# Copyright (C) 2020 - 2024 Thore Tyborski <https://github.com/ThoreBor>
# Copyright (C) 2024 Shigeyuki <http://patreon.com/Shigeyuki>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import datetime
from datetime import date, timedelta

from aqt import mw

from .count_time import shigeTaskTimer

#MARK: get_new_day_and_time_now
def get_new_day_and_time_now():
    
    from .get_rollover import get_rollover_hour
    rolloverHour = get_rollover_hour()

    new_day = datetime.time(rolloverHour, 0, 0)
    time_now = datetime.datetime.now().time()
    
    return new_day, time_now


#MARK: streks v2
def get_streaks_value(new_day, time_now):
    # 💪('ω'💪) 30x speedup!

    current_date = date.today()
    if time_now < new_day:
        # Use previous day if before new day
        current_date -= timedelta(days=1)

    check_date = current_date

    # Get Earliest revlog
    min_revlog_id = mw.col.db.scalar("SELECT MIN(id) FROM revlog")
    if min_revlog_id is None:
        return 0

    # Earliest revlog date
    min_revlog_datetime = datetime.datetime.fromtimestamp(min_revlog_id // 1000)
    oldest_date = min_revlog_datetime.date()

    streak_length = 0
    while check_date >= oldest_date:
        day_start = datetime.datetime.combine(check_date, new_day)
        try:
            day_start_ms = int(day_start.timestamp() * 1000)
        except (OSError, ValueError):
            break

        review_count = mw.col.db.scalar(
            # 1件のみ取得
            "SELECT 1 FROM revlog WHERE id >= ? AND id < ? AND ease > 0 LIMIT 1",
            # 数を取得
            # "SELECT COUNT(*) FROM revlog WHERE id >= ? AND id < ? AND ease > 0",
            day_start_ms, day_start_ms + 24 * 60 * 60 * 1000  # 24h(86,400,000s）
        )

        if review_count:
            streak_length += 1
        else:
            break

        check_date -= timedelta(days=1) # previous day

    return streak_length


#MARK: streak
def streak():

    shigeTaskTimer.start("get_streaks_value")

    new_day, time_now = get_new_day_and_time_now()
    streak_value = get_streaks_value(new_day, time_now)

    shigeTaskTimer.end("get_streaks_value")

    return streak_value

