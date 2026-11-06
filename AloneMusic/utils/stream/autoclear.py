#
# Copyright (C) 2021-2022 by TheAloneteam@Github, < https://github.com/TheAloneTeam >.
#
# This file is part of < https://github.com/TheAloneTeam/AloneMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TheAloneTeam/AloneMusic/blob/master/LICENSE >
#
# All rights reserved.

import os

from config import autoclean


async def auto_clean(popped):
    try:
        rem = popped.get("file")
        if isinstance(rem, str) and rem:
            try:
                autoclean.remove(rem)
            except ValueError:
                pass

            if autoclean.count(rem) == 0 and not any(
                marker in rem for marker in ("vid_", "live_", "index_")
            ):
                try:
                    os.remove(rem)
                except FileNotFoundError:
                    pass
                except OSError:
                    pass
    except Exception:
        pass
    try:
        mystic = popped.get("mystic")
        if mystic:
            await mystic.delete()
    except:
        pass
