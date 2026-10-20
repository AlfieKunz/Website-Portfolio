# Copyright (C) Shigeyuki <http://patreon.com/Shigeyuki>
# License: GNU AGPL version 3 or later <http://www.gnu.org/licenses/agpl.html>

def get_rollover_hour():
    try:
        from aqt import mw
        rolloverHour = mw.col.conf.get("rollover", 4)
        rolloverHour = int(rolloverHour)
        if rolloverHour < 0 or rolloverHour > 23:
            rolloverHour = 4
    except Exception as e:
        print(f"[GetRollover] Error: {e} ")
        rolloverHour = 4
    
    return rolloverHour