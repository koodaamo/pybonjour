import select
import sys
import logging
from contextlib import contextmanager
import pybonjour

from srvdefs import UDP_SERVICES, TCP_SERVICES

logging.basicConfig()
logger = logging.getLogger("bonjour")
logger.setLevel(logging.INFO)

BROWSER = pybonjour.DNSServiceBrowse
RESOLVER = pybonjour.DNSServiceResolve
LISTENER = pybonjour.DNSServiceProcessResult
REFERENCE = pybonjour.DNSServiceRef

def get_service(bjoursrv):
   name, proto = bjoursrv.replace("_", "")[:-1].split(".")
   if proto == "udp":
      return UDP_SERVICES.get(name, name)
   elif proto == "tcp":
      return TCP_SERVICES.get(name, name)
   else:
      raise Exception("wrong protocol: %s" % proto)

class Dispatcher:

   def __init__(self, srvtypes):
      mkref = lambda srvtype: pybonjour.DNSServiceBrowse(regtype=srvtype, callBack=self._handle_event)
      self._registrations = [mkref(srvtype) for srvtype in srvtypes]

   def __iadd__(self, sdref):
      self._registrations.update([sdref])

   def _handle_event(self, sdRef, flags, ifaceidx, error, srvname, regtype, replyfrm):
      "upon a browser event receipt"
      if error != pybonjour.kDNSServiceErr_NoError:
         logger.error("browser error: %s" % str(error))
         return
      if not (flags & pybonjour.kDNSServiceFlagsAdd):
         logger.info("REMOVED: '%s' (%s) at %s" % (srvname, get_service(regtype), replyfrm))
         return
      logger.info("SERVICE: '%s' (%s) at %s" % (srvname, get_service(regtype), replyfrm))

      new_ref = pybonjour.DNSServiceResolve(0, ifaceidx, srvname, regtype, replyfrm, callBack=self._handle_resolved)
      self._registrations.append(new_ref)

   def _handle_resolved(self, sdref, flags, ifaceidx, err, srvname, replyfrm, port, txt):
      "upon resolve reply receipt"
      logger.info("resolved: %s at %s" % (srvname, replyfrm))
      self._registrations.remove(sdref)

   def __call__(self):
      logger.info("---- starting browser ----")
      while True:
         for results in select.select(self._registrations, [], []):
            for sdref in self._registrations:
               if sdref in results:
                  pybonjour.DNSServiceProcessResult(sdref)

if __name__=="__main__":

   d = Dispatcher(sys.argv[1:])
   d()
