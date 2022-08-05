import asyncio

def _set_lock(self):
    self.set_lock = True

def _is_proc_locked(self):
    try:
        return self.set_lock
    except:
        return False

def _set_proc_lock_ack(self):
    self.ack_lock = True

def _is_proc_lock_acked(self):
    try:
        return self.ack_lock
    except:
        return False

async def release_lock(self):
    self.set_lock = False

async def set_lock(self):
    _set_lock(self)
    while not _is_proc_lock_acked(self):
        await asyncio.sleep(0.1)

async def check_lock(self):
    if _is_proc_locked(self):
        _set_proc_lock_ack(self)
        while _is_proc_locked(self):
            await asyncio.sleep(0.1)