import config

def debug(*messages, **kwargs):
  level = kwargs.get("level", 0)
  fp = kwargs.get("fp", sys.stdout)

  if not hasattr(config, "debuglevel"):
    config.debuglevel = level

  if hasattr(config, "debuglevel") and \
  config.debuglevel > level:
    for message in messages:
      fp.write(message)
      if not message.endswith("\n"):
        fp.write("\n")
      fp.flush()

class DebugLog:
  def __init__(self, fp): self.fp = fp
  def __getattr__(self, k):
    if hasattr(self.fp, k): return getattr(self.fp, k)
    raise AttributeError
  def write(self, message, level=0):
    debug(message, fp=self.fp, level=level)
sys.stdout = DebugLog(sys.stdout)
