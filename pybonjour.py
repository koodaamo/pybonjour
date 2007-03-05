################################################################################
#
# Copyright (c) 2007 Christopher J. Stawarz
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
################################################################################



import ctypes
import socket

# FIXME: need to use windll on Windows
_libdnssd = ctypes.cdll.LoadLibrary('libSystem.B.dylib')

# FIXME: need to use WINFUNCTYPE on Windows
_Callback = ctypes.CFUNCTYPE



################################################################################
#
# Constants
#
################################################################################



#
# General flags
#

kDNSServiceFlagsMoreComing          = 0x1
kDNSServiceFlagsAdd                 = 0x2
kDNSServiceFlagsDefault             = 0x4
kDNSServiceFlagsNoAutoRename        = 0x8
kDNSServiceFlagsShared              = 0x10
kDNSServiceFlagsUnique              = 0x20
kDNSServiceFlagsBrowseDomains       = 0x40
kDNSServiceFlagsRegistrationDomains = 0x80
kDNSServiceFlagsLongLivedQuery      = 0x100
kDNSServiceFlagsAllowRemoteQuery    = 0x200
kDNSServiceFlagsForceMulticast      = 0x400
kDNSServiceFlagsReturnCNAME         = 0x800


#
# Service classes
#

kDNSServiceClass_IN                 = 1


#
# Service types
#

kDNSServiceType_A                   = 1
kDNSServiceType_NS                  = 2
kDNSServiceType_MD                  = 3
kDNSServiceType_MF                  = 4
kDNSServiceType_CNAME               = 5
kDNSServiceType_SOA                 = 6
kDNSServiceType_MB                  = 7
kDNSServiceType_MG                  = 8
kDNSServiceType_MR                  = 9
kDNSServiceType_NULL                = 10
kDNSServiceType_WKS                 = 11
kDNSServiceType_PTR                 = 12
kDNSServiceType_HINFO               = 13
kDNSServiceType_MINFO               = 14
kDNSServiceType_MX                  = 15
kDNSServiceType_TXT                 = 16
kDNSServiceType_RP                  = 17
kDNSServiceType_AFSDB               = 18
kDNSServiceType_X25                 = 19
kDNSServiceType_ISDN                = 20
kDNSServiceType_RT                  = 21
kDNSServiceType_NSAP                = 22
kDNSServiceType_NSAP_PTR            = 23
kDNSServiceType_SIG                 = 24
kDNSServiceType_KEY                 = 25
kDNSServiceType_PX                  = 26
kDNSServiceType_GPOS                = 27
kDNSServiceType_AAAA                = 28
kDNSServiceType_LOC                 = 29
kDNSServiceType_NXT                 = 30
kDNSServiceType_EID                 = 31
kDNSServiceType_NIMLOC              = 32
kDNSServiceType_SRV                 = 33
kDNSServiceType_ATMA                = 34
kDNSServiceType_NAPTR               = 35
kDNSServiceType_KX                  = 36
kDNSServiceType_CERT                = 37
kDNSServiceType_A6                  = 38
kDNSServiceType_DNAME               = 39
kDNSServiceType_SINK                = 40
kDNSServiceType_OPT                 = 41
kDNSServiceType_TKEY                = 249
kDNSServiceType_TSIG                = 250
kDNSServiceType_IXFR                = 251
kDNSServiceType_AXFR                = 252
kDNSServiceType_MAILB               = 253
kDNSServiceType_MAILA               = 254
kDNSServiceType_ANY                 = 255


#
# Error codes
#

kDNSServiceErr_NoError              = 0
kDNSServiceErr_Unknown              = -65537
kDNSServiceErr_NoSuchName           = -65538
kDNSServiceErr_NoMemory             = -65539
kDNSServiceErr_BadParam             = -65540
kDNSServiceErr_BadReference         = -65541
kDNSServiceErr_BadState             = -65542
kDNSServiceErr_BadFlags             = -65543
kDNSServiceErr_Unsupported          = -65544
kDNSServiceErr_NotInitialized       = -65545
kDNSServiceErr_AlreadyRegistered    = -65547
kDNSServiceErr_NameConflict         = -65548
kDNSServiceErr_Invalid              = -65549
kDNSServiceErr_Firewall             = -65550
kDNSServiceErr_Incompatible         = -65551
kDNSServiceErr_BadInterfaceIndex    = -65552
kDNSServiceErr_Refused              = -65553
kDNSServiceErr_NoSuchRecord         = -65554
kDNSServiceErr_NoAuth               = -65555
kDNSServiceErr_NoSuchKey            = -65556
kDNSServiceErr_NATTraversal         = -65557
kDNSServiceErr_DoubleNAT            = -65558
kDNSServiceErr_BadTime              = -65559


#
# Other constants
#

kDNSServiceMaxServiceName           = 64
kDNSServiceMaxDomainName            = 1005
kDNSServiceInterfaceIndexAny        = 0
kDNSServiceInterfaceIndexLocalOnly  = -1



################################################################################
#
# Low-level data types
#
################################################################################



#
# FIXME:
#
# According to dns_sd.h, all strings used in DNS-SD are UTF-8 strings.
# What bearing does that have on how such values are passed to and
# from Python (i.e. should we use unicode, or is str okay)?
#


_DNSServiceRef       = ctypes.c_void_p
_DNSRecordRef        = ctypes.c_void_p
_DNSServiceFlags     = ctypes.c_uint32
_DNSServiceErrorType = ctypes.c_int32


_DNSServiceDomainEnumReply = _Callback(
    None,
    _DNSServiceRef,		# sdRef
    _DNSServiceFlags,		# flags
    ctypes.c_uint32,		# interfaceIndex
    _DNSServiceErrorType,	# errorCode
    ctypes.c_char_p,		# replyDomain
    ctypes.c_void_p,		# context
    )


_DNSServiceRegisterReply = _Callback(
    None,
    _DNSServiceRef,		# sdRef
    _DNSServiceFlags,		# flags
    _DNSServiceErrorType,	# errorCode
    ctypes.c_char_p,		# name
    ctypes.c_char_p,		# regtype
    ctypes.c_char_p,		# domain
    ctypes.c_void_p,		# context
    )


_DNSServiceBrowseReply = _Callback(
    None,
    _DNSServiceRef,		# sdRef
    _DNSServiceFlags,		# flags
    ctypes.c_uint32,		# interfaceIndex
    _DNSServiceErrorType,	# errorCode
    ctypes.c_char_p,		# serviceName
    ctypes.c_char_p,		# regtype
    ctypes.c_char_p,		# replyDomain
    ctypes.c_void_p,		# context
    )


_DNSServiceResolveReply = _Callback(
    None,
    _DNSServiceRef,		# sdRef
    _DNSServiceFlags,		# flags
    ctypes.c_uint32,		# interfaceIndex
    _DNSServiceErrorType,	# errorCode
    ctypes.c_char_p,		# fullname
    ctypes.c_char_p,		# hosttarget
    ctypes.c_uint16,		# port
    ctypes.c_uint16,		# txtLen
    ctypes.c_void_p,		# txtRecord (not NULL-terminated, so c_void_p)
    ctypes.c_void_p,		# context
    )


_DNSServiceRegisterRecordReply = _Callback(
    None,
    _DNSServiceRef,		# sdRef
    _DNSRecordRef,		# RecordRef
    _DNSServiceFlags,		# flags
    _DNSServiceErrorType,	# errorCode
    ctypes.c_void_p,		# context
    )


_DNSServiceQueryRecordReply = _Callback(
    None,
    _DNSServiceRef,		# sdRef
    _DNSServiceFlags,		# flags
    ctypes.c_uint32,		# interfaceIndex
    _DNSServiceErrorType,	# errorCode
    ctypes.c_char_p,		# fullname
    ctypes.c_uint16,		# rrtype
    ctypes.c_uint16,		# rrclass
    ctypes.c_uint16,		# rdlen
    ctypes.c_void_p,		# rdata
    ctypes.c_uint32,		# ttl
    ctypes.c_void_p,		# context
    )



################################################################################
#
# Low-level function bindings
#
################################################################################



func_specs = {

    'DNSServiceRefSockFD':
    (
	ctypes.c_int,
	(
	    _DNSServiceRef,			# sdRef
	    )),

    'DNSServiceProcessResult':
    (
	_DNSServiceErrorType,
	(
	    _DNSServiceRef,			# sdRef
	    )),

    'DNSServiceRefDeallocate':
    (
	None,
	(
	    _DNSServiceRef,			# sdRef
	    )),

    'DNSServiceEnumerateDomains':
    (
	_DNSServiceErrorType,
	(
	    ctypes.POINTER(_DNSServiceRef),	# sdRef
	    _DNSServiceFlags,			# flags
	    ctypes.c_uint32,			# interfaceIndex
	    _DNSServiceDomainEnumReply,		# callBack
	    ctypes.c_void_p,			# context
	    )),

    'DNSServiceRegister':
    (
	_DNSServiceErrorType,
	(
	    ctypes.POINTER(_DNSServiceRef),	# sdRef
	    _DNSServiceFlags,			# flags
	    ctypes.c_uint32,			# interfaceIndex
	    ctypes.c_char_p,			# name
	    ctypes.c_char_p,			# regtype
	    ctypes.c_char_p,			# domain
	    ctypes.c_char_p,			# host
	    ctypes.c_uint16,			# port
	    ctypes.c_uint16,			# txtLen
	    ctypes.c_void_p,			# txtRecord
	    _DNSServiceRegisterReply,		# callBack
	    ctypes.c_void_p,			# context
	    )),

    'DNSServiceAddRecord':
    (
	_DNSServiceErrorType,
	(
	    _DNSServiceRef,			# sdRef
	    ctypes.POINTER(_DNSRecordRef),	# RecordRef
	    _DNSServiceFlags,			# flags
	    ctypes.c_uint16,			# rrtype
	    ctypes.c_uint16,			# rdlen
	    ctypes.c_void_p,			# rdata
	    ctypes.c_uint32,			# ttl
	    )),

    'DNSServiceUpdateRecord':
    (
	_DNSServiceErrorType,
	(
	    _DNSServiceRef,			# sdRef
	    _DNSRecordRef,			# RecordRef
	    _DNSServiceFlags,			# flags
	    ctypes.c_uint16,			# rdlen
	    ctypes.c_void_p,			# rdata
	    ctypes.c_uint32,			# ttl
	    )),

    'DNSServiceRemoveRecord':
    (
	_DNSServiceErrorType,
	(
	    _DNSServiceRef,			# sdRef
	    _DNSRecordRef,			# RecordRef
	    _DNSServiceFlags,			# flags
	    )),

    'DNSServiceBrowse':
    (
	_DNSServiceErrorType,
	(
	    ctypes.POINTER(_DNSServiceRef),	# sdRef
	    _DNSServiceFlags,			# flags
	    ctypes.c_uint32,			# interfaceIndex
	    ctypes.c_char_p,			# regtype
	    ctypes.c_char_p,			# domain
	    _DNSServiceBrowseReply,		# callBack
	    ctypes.c_void_p,			# context
	    )),

    'DNSServiceResolve':
    (
	_DNSServiceErrorType,
	(
	    ctypes.POINTER(_DNSServiceRef),	# sdRef
	    _DNSServiceFlags,			# flags
	    ctypes.c_uint32,			# interfaceIndex
	    ctypes.c_char_p,			# name
	    ctypes.c_char_p,			# regtype
	    ctypes.c_char_p,			# domain
	    _DNSServiceResolveReply,		# callBack
	    ctypes.c_void_p,			# context
	    )),

    'DNSServiceCreateConnection':
    (
	_DNSServiceErrorType,
	(
	    ctypes.POINTER(_DNSServiceRef),	# sdRef
	    )),

    'DNSServiceRegisterRecord':
    (
	_DNSServiceErrorType,
	(
	    _DNSServiceRef,			# sdRef
	    ctypes.POINTER(_DNSRecordRef),	# RecordRef
	    _DNSServiceFlags,			# flags
	    ctypes.c_uint32,			# interfaceIndex
	    ctypes.c_char_p,			# fullname
	    ctypes.c_uint16,			# rrtype
	    ctypes.c_uint16,			# rrclass
	    ctypes.c_uint16,			# rdlen
	    ctypes.c_void_p,			# rdata
	    ctypes.c_uint32,			# ttl
	    _DNSServiceRegisterRecordReply,	# callBack
	    ctypes.c_void_p,			# context
	    )),

    'DNSServiceQueryRecord':
    (
	_DNSServiceErrorType,
	(
	    ctypes.POINTER(_DNSServiceRef),	# sdRef
	    _DNSServiceFlags,			# flags
	    ctypes.c_uint32,			# interfaceIndex
	    ctypes.c_char_p,			# fullname
	    ctypes.c_uint16,			# rrtype
	    ctypes.c_uint16,			# rrclass
	    _DNSServiceQueryRecordReply,	# callBack
	    ctypes.c_void_p,			# context
	    )),

    'DNSServiceReconfirmRecord':
    (
	_DNSServiceErrorType,
	(
	    _DNSServiceFlags,			# flags
	    ctypes.c_uint32,			# interfaceIndex
	    ctypes.c_char_p,			# fullname
	    ctypes.c_uint16,			# rrtype
	    ctypes.c_uint16,			# rrclass
	    ctypes.c_uint16,			# rdlen
	    ctypes.c_void_p,			# rdata
	    )),

    'DNSServiceConstructFullName':
    (
	ctypes.c_int,
	(
	    ctypes.c_char * kDNSServiceMaxDomainName,		# fullName
	    ctypes.c_char_p,					# service
	    ctypes.c_char_p,					# regtype
	    ctypes.c_char_p,					# domain
	    )),

    }


_globals = globals()

for name, (restype, argtypes) in func_specs.iteritems():
    func          = getattr(_libdnssd, name)
    func.restype  = restype
    func.argtypes = argtypes
    _globals['_' + name] = func

del func_specs, _globals, name, restype, argtypes, func



################################################################################
#
# Error handling
#
################################################################################



class BonjourError(Exception):

    _errmsg = {
	kDNSServiceErr_Unknown:			'unknown',
	kDNSServiceErr_NoSuchName:		'no such name',
	kDNSServiceErr_NoMemory:		'no memory',
	kDNSServiceErr_BadParam:		'bad param',
	kDNSServiceErr_BadReference:		'bad reference',
	kDNSServiceErr_BadState:		'bad state',
	kDNSServiceErr_BadFlags:		'bad flags',
	kDNSServiceErr_Unsupported:		'unsupported',
	kDNSServiceErr_NotInitialized:		'not initialized',
	kDNSServiceErr_AlreadyRegistered:	'already registered',
	kDNSServiceErr_NameConflict:		'name conflict',
	kDNSServiceErr_Invalid:			'invalid',
	kDNSServiceErr_Firewall:		'firewall',
	kDNSServiceErr_Incompatible:		'incompatible',
	kDNSServiceErr_BadInterfaceIndex:	'bad interface index',
	kDNSServiceErr_Refused:			'refused',
	kDNSServiceErr_NoSuchRecord:		'no such record',
	kDNSServiceErr_NoAuth:			'no auth',
	kDNSServiceErr_NoSuchKey:		'no such key',
	kDNSServiceErr_NATTraversal:		'NAT traversal',
	kDNSServiceErr_DoubleNAT:		'double NAT',
	kDNSServiceErr_BadTime:			'bad time',
	}

    def __init__(self, errorCode, errorMsg=None):
	if errorMsg is None:
	    errorMsg = self._errmsg.get(errorCode, 'unknown error')
	Exception.__init__(self, (errorCode, errorMsg))



################################################################################
#
# High-level data types
#
################################################################################



class DNSRecordRef(object):

    _as_parameter_ = property(lambda self: self._ref)

    def __init__(self, _ref=None):
	self._ref = ctypes.c_void_p(_ref)

    def __eq__(self, other):
	return ((type(other) is type(self)) and
		(other._ref.value == self._ref.value))

    def _byref(self):
	return ctypes.byref(self._ref)

    def _invalidate(self):
	self._ref.value = None

    def _valid(self):
	return (self._ref.value is not None)


class DNSServiceRef(DNSRecordRef):

    def __init__(self, _ref=None):
	DNSRecordRef.__init__(self, _ref)

	# A DNSRecordRef is invalidated if DNSServiceRefDeallocate()
	# is called on the corresponding DNSServiceRef, so we need to
	# keep track of all our record refs and invalidate them when
	# we're closed.
	self._record_refs = []

    def _new_record_ref(self):
	ref = DNSRecordRef()
	self._record_refs.append(ref)
	return ref

    def close(self):
	if self._valid():
	    for ref in self._record_refs:
		ref._invalidate()
	    _DNSServiceRefDeallocate(self)
	    self._invalidate()

    def fileno(self):
	return _DNSServiceRefSockFD(self)



################################################################################
#
# Internal utility types and functions
#
################################################################################



class _NoDefaultType(object):
    def __repr__(self):
	return '<NO DEFAULT VALUE>'

_NO_DEFAULT = _NoDefaultType()


def _string_to_length_and_void_p(string):
    void_p = ctypes.cast(ctypes.c_char_p(string), ctypes.c_void_p)
    return len(string), void_p


def _length_and_void_p_to_string(length, void_p):
    char_p = ctypes.cast(void_p, ctypes.POINTER(ctypes.c_char))
    return ''.join(char_p[i] for i in xrange(length))



################################################################################
#
# High-level functions
#
################################################################################



def DNSServiceProcessResult(sdRef):
    err = _DNSServiceProcessResult(sdRef)
    if err != kDNSServiceErr_NoError:
	raise BonjourError(err)


def DNSServiceEnumerateDomains(
    flags = _NO_DEFAULT,
    interfaceIndex = kDNSServiceInterfaceIndexAny,
    callBack = None,
    ):

    @_DNSServiceDomainEnumReply
    def enumerate_domains_callback(sdRef, flags, interfaceIndex, errorCode,
				   replyDomain, context):
	if callBack is not None:
	    if errorCode != kDNSServiceErr_NoError:
		sdRef, flags, interfaceIndex, replyDomain = (None,) * 4
	    else:
		sdRef = DNSServiceRef(sdRef)
	    callBack(sdRef, flags, interfaceIndex, errorCode, replyDomain)

    sdRef = DNSServiceRef()

    err = _DNSServiceEnumerateDomains(sdRef._byref(),
				      flags,
				      interfaceIndex,
				      enumerate_domains_callback,
				      None)

    if err != kDNSServiceErr_NoError:
	raise BonjourError(err)

    return sdRef


def DNSServiceRegister(
    flags = 0,
    interfaceIndex = kDNSServiceInterfaceIndexAny,
    name = None,
    regtype = _NO_DEFAULT,
    domain = None,
    host = None,
    port = _NO_DEFAULT,
    txtRecord = '',
    callBack = None,
    ):

    @_DNSServiceRegisterReply
    def register_callback(sdRef, flags, errorCode, name, regtype, domain,
			  context):
	if callBack is not None:
	    if errorCode != kDNSServiceErr_NoError:
		sdRef, flags, name, regtype, domain = (None,) * 5
	    else:
		sdRef = DNSServiceRef(sdRef)
	    callBack(sdRef, flags, errorCode, name, regtype, domain)

    sdRef = DNSServiceRef()

    if not txtRecord:
	txtLen, txtRecord = 1, '\0'
    else:
	txtLen, txtRecord = _string_to_length_and_void_p(txtRecord)

    err = _DNSServiceRegister(sdRef._byref(),
			      flags,
			      interfaceIndex,
			      name,
			      regtype,
			      domain,
			      host,
			      socket.htons(port),
			      txtLen,
			      txtRecord,
			      register_callback,
			      None)

    if err != kDNSServiceErr_NoError:
	raise BonjourError(err)

    return sdRef


def DNSServiceBrowse(
    flags = 0,
    interfaceIndex = kDNSServiceInterfaceIndexAny,
    regtype = _NO_DEFAULT,
    domain = None,
    callBack = None,
    ):

    @_DNSServiceBrowseReply
    def browse_callback(sdRef, flags, interfaceIndex, errorCode, serviceName,
			regtype, replyDomain, context):
	if callBack is not None:
	    if errorCode != kDNSServiceErr_NoError:
		(sdRef, flags, interfaceIndex, serviceName, regtype,
		 replyDomain) = (None,) * 6
	    else:
		sdRef = DNSServiceRef(sdRef)
	    callBack(sdRef, flags, interfaceIndex, errorCode, serviceName,
		     regtype, replyDomain)

    sdRef = DNSServiceRef()

    err = _DNSServiceBrowse(sdRef._byref(),
			    flags,
			    interfaceIndex,
			    regtype,
			    domain,
			    browse_callback,
			    None)

    if err != kDNSServiceErr_NoError:
	raise BonjourError(err)

    return sdRef


def DNSServiceResolve(
    flags = 0,
    interfaceIndex = _NO_DEFAULT,
    name = _NO_DEFAULT,
    regtype = _NO_DEFAULT,
    domain = _NO_DEFAULT,
    callBack = None,
    ):

    @_DNSServiceResolveReply
    def resolve_callback(sdRef, flags, interfaceIndex, errorCode, fullname,
			 hosttarget, port, txtLen, txtRecord, context):
	if callBack is not None:
	    if errorCode != kDNSServiceErr_NoError:
		(sdRef, flags, interfaceIndex, fullname, hosttarget, port,
		 txtRecord) = (None,) * 7
	    else:
		sdRef = DNSServiceRef(sdRef)
		port = socket.ntohs(port)
		txtRecord = _length_and_void_p_to_string(txtLen, txtRecord)
	    callBack(sdRef, flags, interfaceIndex, errorCode, fullname,
		     hosttarget, port, txtRecord)

    sdRef = DNSServiceRef()

    err = _DNSServiceResolve(sdRef._byref(),
			     flags,
			     interfaceIndex,
			     name,
			     regtype,
			     domain,
			     resolve_callback,
			     None)

    if err != kDNSServiceErr_NoError:
	raise BonjourError(err)

    return sdRef


def DNSServiceConstructFullName(
    service = None,
    regtype = _NO_DEFAULT, 
    domain = _NO_DEFAULT,
    ):

    fullName = ctypes.create_string_buffer(kDNSServiceMaxDomainName)

    err = _DNSServiceConstructFullName(fullName, service, regtype, domain)

    if err != 0:
	raise BonjourError(err, 'name construction failed')

    return fullName.value



################################################################################
#
# Test routine
#
################################################################################



if __name__ == '__main__':
    import select
    import threading

    enumEvent = threading.Event()

    def enumerate_domains_callback(sdRef, flags, interfaceIndex, errorCode,
				   replyDomain):
	print 'Available domain:', replyDomain
	if not (flags & kDNSServiceFlagsMoreComing):
	    enumEvent.set()

    enum_sdRef = \
	DNSServiceEnumerateDomains(flags=kDNSServiceFlagsRegistrationDomains,
				   callBack=enumerate_domains_callback)

    while not enumEvent.isSet():
	ready = select.select([enum_sdRef], [], [])
	if enum_sdRef in ready[0]:
	    DNSServiceProcessResult(enum_sdRef)

    enum_sdRef.close()

    name = "MyService"
    regtype = "_test._tcp"
    port = 1111

    registerEvent = threading.Event()

    def register_callback(sdRef, flags, errorCode, name, regtype, domain):
	print 'Service registered as %s' % name
	registerEvent.set()

    reg_sdRef = DNSServiceRegister(name=name, regtype=regtype, port=port,
				   callBack=register_callback)

    while not registerEvent.isSet():
	ready = select.select([reg_sdRef], [], [])
	if reg_sdRef in ready[0]:
	    DNSServiceProcessResult(reg_sdRef)

    browseEvent = threading.Event()

    def browse_callback(sdRef, flags, interfaceIndex, errorCode, serviceName,
			regtype, replyDomain):
	if (serviceName == name) and (flags & kDNSServiceFlagsAdd):
	    print 'Found service %s; resolving' % serviceName

	    resolveEvent = threading.Event()

	    def resolve_callback(sdRef, flags, interfaceIndex, errorCode,
				 fullname, hosttarget, port, txtRecord):
		print ('Resolved service %s at %s:%d' % 
		       (fullname, hosttarget, port))
		print "txtRecord = %r" % txtRecord
		resolveEvent.set()

	    resolve_sdRef = DNSServiceResolve(0, interfaceIndex, serviceName,
					      regtype, replyDomain,
					      resolve_callback)

	    while not resolveEvent.isSet():
		ready = select.select([resolve_sdRef], [], [])
		if resolve_sdRef in ready[0]:
		    DNSServiceProcessResult(resolve_sdRef)

	    browseEvent.set()
	    resolve_sdRef.close()

    browse_sdRef = DNSServiceBrowse(regtype=regtype, callBack=browse_callback)

    while not browseEvent.isSet():
	ready = select.select([browse_sdRef], [], [])
	if browse_sdRef in ready[0]:
	    DNSServiceProcessResult(browse_sdRef)

    browse_sdRef.close()
    reg_sdRef.close()
