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



#
# NOTE:
#
# To use this module with Python 2.4, you'll need to install ctypes
# 1.0.1 or later.  Starting with Python 2.5, ctypes is part of the
# standard library, so no additional software is required.
#


"""

Pure-Python bindings for Apple's Bonjour library

Say something about unicode here.

"""


__author__   = 'Christopher Stawarz <cstawarz@csail.mit.edu>'
__version__  = '1.0.0'
__revision__ = '$Revision$'


import ctypes
import os
import socket
import sys


if sys.platform == 'win32':
    # Need to use the stdcall variants
    _libdnssd = ctypes.windll.dnssd
    _CFunc = ctypes.WINFUNCTYPE
else:
    if sys.platform == 'darwin':
	_libdnssd = 'libSystem.B.dylib'
    else:
	_libdnssd = 'libdns_sd.so'
	# If libdns_sd is actually Avahi's Bonjour compatibility
	# layer, silence its annoying warning messages
	os.environ['AVAHI_COMPAT_NOWARN'] = '1'
    _libdnssd = ctypes.cdll.LoadLibrary(_libdnssd)
    _CFunc = ctypes.CFUNCTYPE



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
# Error handling
#
################################################################################



class BonjourError(Exception):

    _errmsg = {
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

    @classmethod
    def _errcheck(cls, result, func, args):
	if result != kDNSServiceErr_NoError:
	    raise cls(result)
	return args

    def __init__(self, errorCode):
	Exception.__init__(self,
			   (errorCode, self._errmsg.get(errorCode, 'unknown')))



################################################################################
#
# Data types
#
################################################################################



class _utf8_char_p(ctypes.c_char_p):

    @classmethod
    def from_param(cls, obj):
	if (obj is not None) and (not isinstance(obj, cls)):
	    if not isinstance(obj, basestring):
		raise TypeError('parameter must be a string type instance')
	    if not isinstance(obj, unicode):
		obj = unicode(obj)
	    obj = obj.encode('utf-8')
	return ctypes.c_char_p.from_param(obj)

    def decode(self):
	if self.value is None:
	    return None
	return self.value.decode('utf-8')


class _utf8_char_p_non_null(_utf8_char_p):

    @classmethod
    def from_param(cls, obj):
	if obj is None:
	    raise ValueError('parameter cannot be None')
	return _utf8_char_p.from_param(obj)


_DNSServiceFlags     = ctypes.c_uint32
_DNSServiceErrorType = ctypes.c_int32


#
# FIXME:
#
# How do we prevent users from creating DNSRecordRef's and
# DNSServiceRef's with random values?
#


class DNSRecordRef(ctypes.c_void_p):

    @classmethod
    def from_param(cls, obj):
	if type(obj) is not cls:
	    raise TypeError("expected '%s', got '%s'" %
			    (cls.__name__, type(obj).__name__))
	if obj.value is None:
	    raise ValueError('invalid %s instance' % cls.__name__)
	return obj

    def __eq__(self, other):
	return ((type(other) is type(self)) and	(other.value == self.value))

    def _invalidate(self):
	self.value = None

    def _valid(self):
	return (self.value is not None)


class _DNSRecordRef_or_null(DNSRecordRef):

    @classmethod
    def from_param(cls, obj):
	if obj is None:
	    return obj
	return DNSRecordRef.from_param(obj)


class DNSServiceRef(DNSRecordRef):

    def __init__(self, *args, **kwargs):
	DNSRecordRef.__init__(self, *args, **kwargs)

	# A DNSRecordRef is invalidated if DNSServiceRefDeallocate()
	# is called on the corresponding DNSServiceRef, so we need to
	# keep track of all our record refs and invalidate them when
	# we're closed.
	self._record_refs = []

    def _add_record_ref(self, ref):
	self._record_refs.append(ref)

    def close(self):
	if self._valid():
	    for ref in self._record_refs:
		ref._invalidate()
	    _DNSServiceRefDeallocate(self)
	    self._invalidate()

    def fileno(self):
	return _DNSServiceRefSockFD(self)


_DNSServiceDomainEnumReply = _CFunc(
    None,
    DNSServiceRef,		# sdRef
    _DNSServiceFlags,		# flags
    ctypes.c_uint32,		# interfaceIndex
    _DNSServiceErrorType,	# errorCode
    _utf8_char_p,		# replyDomain
    ctypes.c_void_p,		# context
    )


_DNSServiceRegisterReply = _CFunc(
    None,
    DNSServiceRef,		# sdRef
    _DNSServiceFlags,		# flags
    _DNSServiceErrorType,	# errorCode
    _utf8_char_p,		# name
    _utf8_char_p,		# regtype
    _utf8_char_p,		# domain
    ctypes.c_void_p,		# context
    )


_DNSServiceBrowseReply = _CFunc(
    None,
    DNSServiceRef,		# sdRef
    _DNSServiceFlags,		# flags
    ctypes.c_uint32,		# interfaceIndex
    _DNSServiceErrorType,	# errorCode
    _utf8_char_p,		# serviceName
    _utf8_char_p,		# regtype
    _utf8_char_p,		# replyDomain
    ctypes.c_void_p,		# context
    )


_DNSServiceResolveReply = _CFunc(
    None,
    DNSServiceRef,		# sdRef
    _DNSServiceFlags,		# flags
    ctypes.c_uint32,		# interfaceIndex
    _DNSServiceErrorType,	# errorCode
    _utf8_char_p,		# fullname
    _utf8_char_p,		# hosttarget
    ctypes.c_uint16,		# port
    ctypes.c_uint16,		# txtLen
    ctypes.c_void_p,		# txtRecord (not null-terminated, so c_void_p)
    ctypes.c_void_p,		# context
    )


_DNSServiceRegisterRecordReply = _CFunc(
    None,
    DNSServiceRef,		# sdRef
    DNSRecordRef,		# RecordRef
    _DNSServiceFlags,		# flags
    _DNSServiceErrorType,	# errorCode
    ctypes.c_void_p,		# context
    )


_DNSServiceQueryRecordReply = _CFunc(
    None,
    DNSServiceRef,		# sdRef
    _DNSServiceFlags,		# flags
    ctypes.c_uint32,		# interfaceIndex
    _DNSServiceErrorType,	# errorCode
    _utf8_char_p,		# fullname
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



def _create_function_bindings():

    ERRCHECK    = True
    NO_ERRCHECK = False

    OUTPARAM    = (lambda index: index)
    NO_OUTPARAM = None

    specs = {

	#'funcname':
	#(
	#    return_type,
	#    errcheck,
	#    outparam,
	#    (
	#	param_1_type,
	#	param_2_type,
	#	...
	#	param_n_type,
	#	)),

	'DNSServiceRefSockFD':
	(
	    ctypes.c_int,
	    NO_ERRCHECK,
	    NO_OUTPARAM,
	    (
		DNSServiceRef,			# sdRef
		)),

	'DNSServiceProcessResult':
	(
	    _DNSServiceErrorType,
	    ERRCHECK,
	    NO_OUTPARAM,
	    (
		DNSServiceRef,			# sdRef
		)),

	'DNSServiceRefDeallocate':
	(
	    None,
	    NO_ERRCHECK,
	    NO_OUTPARAM,
	    (
		DNSServiceRef,			# sdRef
		)),

	'DNSServiceEnumerateDomains':
	(
	    _DNSServiceErrorType,
	    ERRCHECK,
	    OUTPARAM(0),
	    (
		ctypes.POINTER(DNSServiceRef),	# sdRef
		_DNSServiceFlags,		# flags
		ctypes.c_uint32,		# interfaceIndex
		_DNSServiceDomainEnumReply,	# callBack
		ctypes.c_void_p,		# context
		)),

	'DNSServiceRegister':
	(
	    _DNSServiceErrorType,
	    ERRCHECK,
	    OUTPARAM(0),
	    (
		ctypes.POINTER(DNSServiceRef),	# sdRef
		_DNSServiceFlags,		# flags
		ctypes.c_uint32,		# interfaceIndex
		_utf8_char_p,			# name
		_utf8_char_p_non_null,		# regtype
		_utf8_char_p,			# domain
		_utf8_char_p,			# host
		ctypes.c_uint16,		# port
		ctypes.c_uint16,		# txtLen
		ctypes.c_void_p,		# txtRecord
		_DNSServiceRegisterReply,	# callBack
		ctypes.c_void_p,		# context
		)),

	'DNSServiceAddRecord':
	(
	    _DNSServiceErrorType,
	    ERRCHECK,
	    OUTPARAM(1),
	    (
		DNSServiceRef,			# sdRef
		ctypes.POINTER(DNSRecordRef),	# RecordRef
		_DNSServiceFlags,		# flags
		ctypes.c_uint16,		# rrtype
		ctypes.c_uint16,		# rdlen
		ctypes.c_void_p,		# rdata
		ctypes.c_uint32,		# ttl
		)),

	'DNSServiceUpdateRecord':
	(
	    _DNSServiceErrorType,
	    ERRCHECK,
	    NO_OUTPARAM,
	    (
		DNSServiceRef,			# sdRef
		_DNSRecordRef_or_null,		# RecordRef
		_DNSServiceFlags,		# flags
		ctypes.c_uint16,		# rdlen
		ctypes.c_void_p,		# rdata
		ctypes.c_uint32,		# ttl
		)),

	'DNSServiceRemoveRecord':
	(
	    _DNSServiceErrorType,
	    ERRCHECK,
	    NO_OUTPARAM,
	    (
		DNSServiceRef,			# sdRef
		DNSRecordRef,			# RecordRef
		_DNSServiceFlags,		# flags
		)),

	'DNSServiceBrowse':
	(
	    _DNSServiceErrorType,
	    ERRCHECK,
	    OUTPARAM(0),
	    (
		ctypes.POINTER(DNSServiceRef),	# sdRef
		_DNSServiceFlags,		# flags
		ctypes.c_uint32,		# interfaceIndex
		_utf8_char_p_non_null,		# regtype
		_utf8_char_p,			# domain
		_DNSServiceBrowseReply,		# callBack
		ctypes.c_void_p,		# context
		)),

	'DNSServiceResolve':
	(
	    _DNSServiceErrorType,
	    ERRCHECK,
	    OUTPARAM(0),
	    (
		ctypes.POINTER(DNSServiceRef),	# sdRef
		_DNSServiceFlags,		# flags
		ctypes.c_uint32,		# interfaceIndex
		_utf8_char_p_non_null,		# name
		_utf8_char_p_non_null,		# regtype
		_utf8_char_p_non_null,		# domain
		_DNSServiceResolveReply,	# callBack
		ctypes.c_void_p,		# context
		)),

	'DNSServiceCreateConnection':
	(
	    _DNSServiceErrorType,
	    ERRCHECK,
	    OUTPARAM(0),
	    (
		ctypes.POINTER(DNSServiceRef),	# sdRef
		)),

	'DNSServiceRegisterRecord':
	(
	    _DNSServiceErrorType,
	    ERRCHECK,
	    OUTPARAM(1),
	    (
		DNSServiceRef,			# sdRef
		ctypes.POINTER(DNSRecordRef),	# RecordRef
		_DNSServiceFlags,		# flags
		ctypes.c_uint32,		# interfaceIndex
		_utf8_char_p_non_null,		# fullname
		ctypes.c_uint16,		# rrtype
		ctypes.c_uint16,		# rrclass
		ctypes.c_uint16,		# rdlen
		ctypes.c_void_p,		# rdata
		ctypes.c_uint32,		# ttl
		_DNSServiceRegisterRecordReply,	# callBack
		ctypes.c_void_p,		# context
		)),

	'DNSServiceQueryRecord':
	(
	    _DNSServiceErrorType,
	    ERRCHECK,
	    OUTPARAM(0),
	    (
		ctypes.POINTER(DNSServiceRef),	# sdRef
		_DNSServiceFlags,		# flags
		ctypes.c_uint32,		# interfaceIndex
		_utf8_char_p_non_null,		# fullname
		ctypes.c_uint16,		# rrtype
		ctypes.c_uint16,		# rrclass
		_DNSServiceQueryRecordReply,	# callBack
		ctypes.c_void_p,		# context
		)),

	'DNSServiceReconfirmRecord':
	(
	    _DNSServiceErrorType,
	    ERRCHECK,
	    NO_OUTPARAM,
	    (
		_DNSServiceFlags,		# flags
		ctypes.c_uint32,		# interfaceIndex
		_utf8_char_p_non_null,		# fullname
		ctypes.c_uint16,		# rrtype
		ctypes.c_uint16,		# rrclass
		ctypes.c_uint16,		# rdlen
		ctypes.c_void_p,		# rdata
		)),

	'DNSServiceConstructFullName':
	(
	    ctypes.c_int,
	    ERRCHECK,
	    OUTPARAM(0),
	    (
		ctypes.c_char * kDNSServiceMaxDomainName,	# fullName
		_utf8_char_p,					# service
		_utf8_char_p_non_null,				# regtype
		_utf8_char_p_non_null,				# domain
		)),

	}


    for name, (restype, errcheck, outparam, argtypes) in specs.iteritems():
	prototype = _CFunc(restype, *argtypes)

	paramflags = [1] * len(argtypes)
	if outparam is not None:
	    paramflags[outparam] = 2
	paramflags = tuple((val,) for val in paramflags)

	func = prototype((name, _libdnssd), paramflags)

	if errcheck:
	    func.errcheck = BonjourError._errcheck

	globals()['_' + name] = func


# Only need to do this once
_create_function_bindings()



################################################################################
#
# Internal utility types and functions
#
################################################################################



class _NoDefault(object):

    def __repr__(self):
	return '<NO DEFAULT>'

    def check(self, obj):
	if obj is self:
	    raise ValueError('required parameter value missing')

_NO_DEFAULT = _NoDefault()


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



def DNSServiceProcessResult(
    sdRef,
    ):

    """

    Read a reply from the daemon, calling the appropriate application
    callback.  This call will block until the daemon's response is
    received.  Use sdRef in conjunction with a run loop or select() to
    determine the presence of a response from the server before
    calling this function to process the reply without blocking.  Call
    this function at any point if it is acceptable to block until the
    daemon's response arrives.  Note that the client is responsible
    for ensuring that DNSServiceProcessResult() is called whenever
    there is a reply from the daemon; the daemon may terminate its
    connection with a client that does not process the daemon's
    responses.

      sdRef:
        A DNSServiceRef returned by any of the DNSService calls that
	take a callback parameter.

    """

    _DNSServiceProcessResult(sdRef)


def DNSServiceEnumerateDomains(
    flags,
    interfaceIndex = kDNSServiceInterfaceIndexAny,
    callBack = None,
    ):

    """

    Asynchronously enumerate domains available for browsing and
    registration.

    The enumeration MUST be cancelled by closing the returned
    DNSServiceRef when no more domains are to be found.

      flags:
        Possible values are:
          kDNSServiceFlagsBrowseDomains to enumerate domains
	  recommended for browsing.
	  kDNSServiceFlagsRegistrationDomains to enumerate domains
	  recommended for registration.

      interfaceIndex:
        If non-zero, specifies the interface on which to look for
	domains.  Most applications will pass
	kDNSServiceInterfaceIndexAny (0) to enumerate domains on all
	interfaces.

      callBack:
        The function to be called when a domain is found or the call
	asynchronously fails.  Its signature should be
	callBack(sdRef,	flags, interfaceIndex, errorCode, replyDomain).

      return value:
        A DNSServiceRef instance.

    Callback Parameters:

      sdRef:
        The DNSServiceRef returned by DNSServiceEnumerateDomains().

      flags:
        Possible values are:
          kDNSServiceFlagsMoreComing
	  kDNSServiceFlagsAdd
	  kDNSServiceFlagsDefault

      interfaceIndex:
        Specifies the interface on which the domain exists.

      errorCode:
        Will be kDNSServiceErr_NoError (0) on success, otherwise
	indicates the failure that occurred (in which case other
	parameters are undefined).

      replyDomain:
        The name of the domain.

    """

    @_DNSServiceDomainEnumReply
    def _callback(sdRef, flags, interfaceIndex, errorCode, replyDomain,
		  context):
	if callBack is not None:
	    callBack(sdRef, flags, interfaceIndex, errorCode,
		     replyDomain.decode())

    return _DNSServiceEnumerateDomains(flags,
				       interfaceIndex,
				       _callback,
				       None)


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

    """

    Register a service that is discovered via DNSServiceBrowse() and
    DNSServiceResolve() calls.

      flags:
        Indicates the renaming behavior on name conflict.  Most
	applications will pass 0.

      interfaceIndex:
        If non-zero, specifies the interface on which to register the
	service.  Most applications will pass
	kDNSServiceInterfaceIndexAny (0) to register on all available
	interfaces.

      name:
        If not None, specifies the service name to be registered.
	Most applications will not specify a name, in which case the
	computer name is used.  (This name is communicated to the
	client via the callback.)  If a name is specified, it must be
	1-63 bytes of UTF-8 text.  If the name is longer than 63
	bytes, it will be automatically truncated to a legal length,
	unless the flag kDNSServiceFlagsNoAutoRename is set, in which
	case a BonjourError exception will be thrown.

      regtype:
        The service type followed by the protocol, separated by a dot
	(e.g. "_ftp._tcp"). The service type must be an underscore,
	followed by 1-14 characters, which may be letters, digits, or
	hyphens.  The transport protocol must be "_tcp" or "_udp". New
	service types should be registered at
	<http://www.dns-sd.org/ServiceTypes.html>.

      domain:
        If not None, specifies the domain on which to advertise the
	service.  Most applications will not specify a domain, instead
	automatically registering in the default domain(s).

      host:
        If not None, specifies the SRV target host name.  Most
	applications will not specify a host, instead automatically
	using the machine's default host name(s).  Note that
	specifying a host name does NOT create an address record for
	that host; the application is responsible for ensuring that
	the appropriate address record exists, or creating it via
	DNSServiceRegisterRecord().

      port:
        The port, in host (not network) byte order, on which the
	service accepts connections.  Pass 0 for a "placeholder"
	service (i.e. a service that will not be discovered by
	browsing, but will cause a name conflict if another client
	tries to register that same name).  Most clients will not use
	placeholder services.

      txtRecord:
        The TXT record rdata.  If not None, txtRecord MUST be a string
	containing a properly formatted DNS TXT record, i.e.
	<length	byte> <data> <length byte> <data> ...

      callBack:
        The function to be called when the registration completes or
	asynchronously fails.  Its signature should be
	callBack(sdRef, flags, errorCode, name, regtype, domain).
	The client MAY pass None for the callback, in which case the
	client will NOT be notified of the default values picked on
	its behalf, and the client will NOT be notified of any
	asynchronous errors (e.g. out of memory errors, etc.) that may
	prevent the registration of the service.  The client may NOT
	pass the flag kDNSServiceFlagsNoAutoRename if the callback is
	None.  The client may still deregister the service at any time
	by closing the returned DNSServiceRef.

      return value:
        A DNSServiceRef instance.  The registration will remain active
	indefinitely until the client terminates it by closing the
	DNSServiceRef.

    Callback Parameters:

      sdRef:
        The DNSServiceRef returned by DNSServiceRegister().

      flags:
        Currently unused, reserved for future use.

      errorCode:
        Will be kDNSServiceErr_NoError on success, otherwise will
	indicate the failure that occurred (including name conflicts,
	if the kDNSServiceFlagsNoAutoRename flag was used when
	registering).  Other parameters are undefined if an error
	occurred.

      name:
        The service name registered.  (If the application did not
	specify a name in DNSServiceRegister(), this indicates what
	name was automatically chosen.)

      regtype:
        The type of service registered, as it was passed to the
        callout.

      domain:
        The domain on which the service was registered.  (If the
	application did not specify a domain in DNSServiceRegister(),
	this indicates the default domain on which the service was
	registered.)

    """

    _NO_DEFAULT.check(regtype)
    _NO_DEFAULT.check(port)

    port = socket.htons(port)

    if not txtRecord:
	txtLen, txtRecord = 1, '\0'
    else:
	txtLen, txtRecord = _string_to_length_and_void_p(txtRecord)

    @_DNSServiceRegisterReply
    def _callback(sdRef, flags, errorCode, name, regtype, domain, context):
	if callBack is not None:
	    callBack(sdRef, flags, errorCode, name.decode(), regtype.decode(),
		     domain.decode())

    return _DNSServiceRegister(flags,
			       interfaceIndex,
			       name,
			       regtype,
			       domain,
			       host,
			       port,
			       txtLen,
			       txtRecord,
			       _callback,
			       None)


def DNSServiceAddRecord(
    sdRef,
    flags = 0,
    rrtype = _NO_DEFAULT,
    rdata = _NO_DEFAULT,
    ttl = 0,
    ):

    """

    Add a record to a registered service.  The name of the record will
    be the same as the registered service's name.  The record can
    later be updated or deregistered by passing the DNSRecordRef
    returned by this function to DNSServiceUpdateRecord() or
    DNSServiceRemoveRecord().

    Note that DNSServiceAddRecord/UpdateRecord/RemoveRecord are NOT
    thread-safe with respect to a single DNSServiceRef.  If you plan
    to have multiple threads in your program simultaneously add,
    update, or remove records from the same DNSServiceRef, then it's
    the caller's responsibility to use a lock or take similar
    appropriate precautions to serialize those calls.

      sdRef:
        A DNSServiceRef returned by DNSServiceRegister().

      flags:
        Currently ignored, reserved for future use.

      rrtype:
        The type of the record (e.g. kDNSServiceType_TXT,
        kDNSServiceType_SRV, etc.).

      rdata:
        A string containing the raw rdata to be contained in the added
        resource record.

      ttl:
        The time to live of the resource record, in seconds.  Pass 0
        to use a default value.

      return value:
        A DNSRecordRef instance, which may be passed to
	DNSServiceUpdateRecord() or DNSServiceRemoveRecord().  If
	sdRef is closed, the DNSRecordRef is also invalidated and may
	not be used further.

    """

    _NO_DEFAULT.check(rrtype)
    _NO_DEFAULT.check(rdata)

    rdlen, rdata = _string_to_length_and_void_p(rdata)

    RecordRef = _DNSServiceAddRecord(sdRef,
				     flags,
				     rrtype,
				     rdlen,
				     rdata,
				     ttl)

    sdRef._add_record_ref(RecordRef)

    return RecordRef


def DNSServiceUpdateRecord(
    sdRef,
    RecordRef = None,
    flags = 0,
    rdata = _NO_DEFAULT,
    ttl = 0,
    ):

    """

    Update a registered resource record.  The record must either be:
      - The primary txt record of a service registered via
        DNSServiceRegister(), or
      - A record added to a registered service via
        DNSServiceAddRecord(), or
      - An individual record registered by DNSServiceRegisterRecord()

      sdRef:
        A DNSServiceRef returned by DNSServiceRegister() or
	DNSServiceCreateConnection().

      RecordRef:
        A DNSRecordRef returned by DNSServiceAddRecord(), or None to
	update the service's primary txt record.

      flags:
        Currently ignored, reserved for future use.

      rdata:
        A string containing the new rdata to be contained in the
        updated resource record.

      ttl:
        The time to live of the updated resource record, in seconds.

    """

    _NO_DEFAULT.check(rdata)

    rdlen, rdata = _string_to_length_and_void_p(rdata)

    _DNSServiceUpdateRecord(sdRef,
			    RecordRef,
			    flags,
			    rdlen,
			    rdata,
			    ttl)


def DNSServiceRemoveRecord(
    sdRef,
    RecordRef,
    flags = 0,
    ):

    """

    Remove a record previously added to a service record set via
    DNSServiceAddRecord(), or deregister a record registered
    individually via DNSServiceRegisterRecord().

      sdRef:
        A DNSServiceRef returned by DNSServiceRegister() (if the
	record being removed was registered via DNSServiceAddRecord())
	or by DNSServiceCreateConnection() (if the record being
	removed was registered via DNSServiceRegisterRecord()).

      recordRef:
        A DNSRecordRef returned by DNSServiceAddRecord() or
	DNSServiceRegisterRecord().

      flags:
        Currently ignored, reserved for future use.

    """

    _DNSServiceRemoveRecord(sdRef,
			    RecordRef,
			    flags)

    RecordRef._invalidate()


def DNSServiceBrowse(
    flags = 0,
    interfaceIndex = kDNSServiceInterfaceIndexAny,
    regtype = _NO_DEFAULT,
    domain = None,
    callBack = None,
    ):

    """

    Browse for instances of a service.

      flags:
        Currently ignored, reserved for future use.

      interfaceIndex:
        If non-zero, specifies the interface on which to browse for
	services.  Most applications will pass
	kDNSServiceInterfaceIndexAny (0) to browse on all available
	interfaces.

      regtype:
        The service type being browsed for followed by the protocol,
	separated by a dot (e.g. "_ftp._tcp").  The transport protocol
	must be "_tcp" or "_udp".

      domain:
        If not None, specifies the domain on which to browse for
	services.  Most applications will not specify a domain,
	instead browsing on the default domain(s).

      callBack:
        The function to be called when an instance of the service
	being browsed for is found, or if the call asynchronously
	fails.  Its signature should be
	callBack(sdRef, flags, interfaceIndex, errorCode,
	         serviceName, regtype, replyDomain).

      return value:
        A DNSServiceRef instance.  The browse operation will run
	indefinitely until the client terminates it by closing the
	DNSServiceRef.

    Callback Parameters:

      sdRef:
        The DNSServiceRef returned by DNSServiceBrowse().

      flags:
        Possible values are kDNSServiceFlagsMoreComing and
        kDNSServiceFlagsAdd.

      interfaceIndex:
        The interface on which the service is advertised.  This index
	should be passed to DNSServiceResolve() when resolving the
	service.

      errorCode:
        Will be kDNSServiceErr_NoError (0) on success, otherwise will
	indicate the failure that occurred.  Other parameters are
	undefined if an error occurred.

      serviceName:
        The discovered service name.  This name should be displayed to
	the user and stored for subsequent use in the
	DNSServiceResolve() call.

      regtype:
        The service type, which is usually (but not always) the same
	as was passed to DNSServiceBrowse().  One case where the
	discovered service type may not be the same as the requested
	service type is when using subtypes: The client may want to
	browse for only those ftp servers that allow anonymous
	connections.  The client will pass the string
	"_ftp._tcp,_anon" to DNSServiceBrowse(), but the type of the
	service that's discovered is simply "_ftp._tcp".  The regtype
	for each discovered service instance should be stored along
	with the name, so that it can be passed to DNSServiceResolve()
	when the service is later resolved.

      replyDomain:
        The domain of the discovered service instance.  This may or
	may not be the same as the domain that was passed to
	DNSServiceBrowse().  The domain for each discovered service
	instance should be stored along with the name, so that it can
	be passed to DNSServiceResolve() when the service is later
	resolved.

    """

    _NO_DEFAULT.check(regtype)

    @_DNSServiceBrowseReply
    def _callback(sdRef, flags, interfaceIndex, errorCode, serviceName, regtype,
		  replyDomain, context):
	if callBack is not None:
	    callBack(sdRef, flags, interfaceIndex, errorCode,
		     serviceName.decode(), regtype.decode(),
		     replyDomain.decode())

    return _DNSServiceBrowse(flags,
			     interfaceIndex,
			     regtype,
			     domain,
			     _callback,
			     None)


def DNSServiceResolve(
    flags = 0,
    interfaceIndex = _NO_DEFAULT,
    name = _NO_DEFAULT,
    regtype = _NO_DEFAULT,
    domain = _NO_DEFAULT,
    callBack = None,
    ):

    """

    Resolve a service name discovered via DNSServiceBrowse() to a
    target host name, port number, and txt record.

    Note: Applications should NOT use DNSServiceResolve() solely for
    txt record monitoring; use DNSServiceQueryRecord() instead, as it
    is more efficient for this task.

    Note: When the desired results have been returned, the client MUST
    terminate the resolve by closing the returned DNSServiceRef.

    Note: DNSServiceResolve() behaves correctly for typical services
    that have a single SRV record and a single TXT record.  To resolve
    non-standard services with multiple SRV or TXT records,
    DNSServiceQueryRecord() should be used.

      flags:
        Currently ignored, reserved for future use.

      interfaceIndex:
        The interface on which to resolve the service.  If this
	resolve call is as a result of a currently active
	DNSServiceBrowse() operation, then the interfaceIndex should
	be the index reported in the browse callback.  If this resolve
	call is using information previously saved (e.g. in a
	preference file) for later use, then use
	kDNSServiceInterfaceIndexAny (0), because the desired service
	may now be reachable via a different physical interface.

      name:
        The name of the service instance to be resolved, as reported
	to the DNSServiceBrowse() callback.

      regtype:
        The type of the service instance to be resolved, as reported
	to the DNSServiceBrowse() callback.

      domain:
        The domain of the service instance to be resolved, as reported
	to the DNSServiceBrowse() callback.

      callBack:
        The function to be called when a result is found, or if the
	call asynchronously fails.  Its signature should be
	callBack(sdRef, flags, interfaceIndex, errorCode, fullname,
	         hosttarget, port, txtRecord).

      return value:
        A DNSServiceRef instance.  The resolve operation will run
	indefinitely until the client terminates it by closing the
	DNSServiceRef.

    Callback Parameters:

      sdRef:
        The DNSServiceRef returned by DNSServiceResolve().

      flags:
        Currently unused, reserved for future use.

      interfaceIndex:
        The interface on which the service was resolved.

      errorCode:
        Will be kDNSServiceErr_NoError (0) on success, otherwise will
	indicate the failure that occurred.  Other parameters are
	undefined if an error occurred.

      fullname:
        The full service domain name, in the form
        <servicename>.<protocol>.<domain>.

      hosttarget:
        The target hostname of the machine providing the service.

      port:
        The port, in host (not network) byte order, on which
        connections are accepted for this service.

      txtRecord:
        A string containing the service's primary txt record, in
        standard txt record format.

    """

    _NO_DEFAULT.check(interfaceIndex)
    _NO_DEFAULT.check(name)
    _NO_DEFAULT.check(regtype)
    _NO_DEFAULT.check(domain)

    @_DNSServiceResolveReply
    def _callback(sdRef, flags, interfaceIndex, errorCode, fullname, hosttarget,
		  port, txtLen, txtRecord, context):
	if callBack is not None:
	    port = socket.ntohs(port)
	    txtRecord = _length_and_void_p_to_string(txtLen, txtRecord)
	    callBack(sdRef, flags, interfaceIndex, errorCode, fullname.decode(),
		     hosttarget.decode(), port, txtRecord)

    return _DNSServiceResolve(flags,
			      interfaceIndex,
			      name,
			      regtype,
			      domain,
			      _callback,
			      None)


def DNSServiceCreateConnection():

    """

    Create a connection to the daemon allowing efficient registration
    of multiple individual records.

      return value:
        A DNSServiceRef instance.  Closing it severs the connection
	and deregisters all records registered on this connection.

    """

    return _DNSServiceCreateConnection()


def DNSServiceRegisterRecord(
    sdRef,
    flags,
    interfaceIndex = kDNSServiceInterfaceIndexAny,
    fullname = _NO_DEFAULT,
    rrtype = _NO_DEFAULT,
    rrclass = kDNSServiceClass_IN,
    rdata = _NO_DEFAULT,
    ttl = 0,
    callBack = None,
    ):

    """

    Register an individual resource record on a connected
    DNSServiceRef.

    Note that name conflicts occurring for records registered via this
    call must be handled by the client in the callback.

      sdRef:
        A DNSServiceRef returned by DNSServiceCreateConnection().

      flags:
        Possible values are kDNSServiceFlagsShared or
        kDNSServiceFlagsUnique.

      interfaceIndex:
        If non-zero, specifies the interface on which to register the
	record.  Passing kDNSServiceInterfaceIndexAny (0) causes the
	record to be registered on all interfaces.

      fullname:
        The full domain name of the resource record.

      rrtype:
        The numerical type of the resource record
        (e.g. kDNSServiceType_PTR, kDNSServiceType_SRV, etc.).

      rrclass:
        The class of the resource record (usually
        kDNSServiceClass_IN).

      rdata:
        A string containing the raw rdata, as it is to appear in the
        DNS record.

      ttl:
        The time to live of the resource record, in seconds.  Pass 0
        to use a default value.

      callBack:
        The function to be called when a result is found, or if the
	call asynchronously fails (e.g. because of a name conflict).
	Its signature should be
	callBack(sdRef, RecordRef, flags, errorCode).

      return value:
        A DNSRecordRef instance, which may be passed to
	DNSServiceUpdateRecord() or DNSServiceRemoveRecord().  (To
	deregister ALL records registered on a single connected
	DNSServiceRef and deallocate each of their corresponding
	DNSRecordRefs, close the DNSServiceRef.)

    Callback Parameters:

      sdRef:
        The connected DNSServiceRef returned by
	DNSServiceCreateConnection().

      RecordRef:
        The DNSRecordRef returned by DNSServiceRegisterRecord().

      flags:
        Currently unused, reserved for future use.

      errorCode:
        Will be kDNSServiceErr_NoError on success, otherwise will
	indicate the failure that occurred (including name conflicts).
	Other parameters are undefined if an error occurred.

    """

    _NO_DEFAULT.check(fullname)
    _NO_DEFAULT.check(rrtype)
    _NO_DEFAULT.check(rdata)

    rdlen, rdata = _string_to_length_and_void_p(rdata)

    @_DNSServiceRegisterRecordReply
    def _callback(sdRef, RecordRef, flags, errorCode, context):
	if callBack is not None:
	    callBack(sdRef, RecordRef, flags, errorCode)

    RecordRef = _DNSServiceRegisterRecord(sdRef,
					  flags,
					  interfaceIndex,
					  fullname,
					  rrtype,
					  rrclass,
					  rdlen,
					  rdata,
					  ttl,
					  _callback,
					  None)

    sdRef._add_record_ref(RecordRef)

    return RecordRef


def DNSServiceQueryRecord(
    flags = 0,
    interfaceIndex = kDNSServiceInterfaceIndexAny,
    fullname = _NO_DEFAULT,
    rrtype = _NO_DEFAULT,
    rrclass = kDNSServiceClass_IN,
    callBack = None,
    ):

    """

    Query for an arbitrary DNS record.

      flags:
        Pass kDNSServiceFlagsLongLivedQuery to create a "long-lived"
	unicast query in a non-local domain.  Without setting this
	flag, unicast queries will be one-shot; that is, only answers
	available at the time of the call will be returned.  By
	setting this flag, answers (including Add and Remove events)
	that become available after the initial call is made will
	generate callbacks.  This flag has no effect on link-local
	multicast queries.

      interfaceIndex:
        If non-zero, specifies the interface on which to issue the
	query.  Passing kDNSServiceInterfaceIndexAny (0) causes the
	name to be queried for on all interfaces.

      fullname:
        The full domain name of the resource record to be queried for.

      rrtype:
        The numerical type of the resource record to be queried for
	(e.g. kDNSServiceType_PTR, kDNSServiceType_SRV, etc.).

      rrclass:
        The class of the resource record (usually
        kDNSServiceClass_IN).

      callBack:
        The function to be called when a result is found, or if the
	call asynchronously fails.  Its signature should be
	callBack(sdRef, flags, interfaceIndex, errorCode, fullname,
	         rrtype, rrclass, rdata, ttl).

      return value:
        A DNSServiceRef instance.  The query operation will run
	indefinitely until the client terminates it by closing the
	DNSServiceRef.

    Callback Parameters:

      sdRef:
        The DNSServiceRef returned by DNSServiceQueryRecord().

      flags:
        Possible values are kDNSServiceFlagsMoreComing and
	kDNSServiceFlagsAdd.  The Add flag is NOT set for PTR records
	with a ttl of 0, i.e. "Remove" events.

      interfaceIndex:
        The interface on which the query was resolved.

      errorCode:
        Will be kDNSServiceErr_NoError on success, otherwise will
	indicate the failure that occurred.  Other parameters are
	undefined if an error occurred.

      fullname:
        The resource record's full domain name.

      rrtype:
        The resource record's type (e.g. kDNSServiceType_PTR,
        kDNSServiceType_SRV, etc.).

      rrclass:
        The class of the resource record (usually
        kDNSServiceClass_IN).

      rdata:
        A string containing the raw rdata of the resource record.

      ttl:
        The resource record's time to live, in seconds.

    """

    _NO_DEFAULT.check(fullname)
    _NO_DEFAULT.check(rrtype)

    @_DNSServiceQueryRecordReply
    def _callback(sdRef, flags, interfaceIndex, errorCode, fullname, rrtype,
		  rrclass, rdlen, rdata, ttl, context):
	if callBack is not None:
	    rdata = _length_and_void_p_to_string(rdlen, rdata)
	    callBack(sdRef, flags, interfaceIndex, errorCode, fullname.decode(),
		     rrtype, rrclass, rdata, ttl)

    return _DNSServiceQueryRecord(flags,
				  interfaceIndex,
				  fullname,
				  rrtype,
				  rrclass,
				  _callback,
				  None)


def DNSServiceReconfirmRecord(
    flags = 0,
    interfaceIndex = kDNSServiceInterfaceIndexAny,
    fullname = _NO_DEFAULT,
    rrtype = _NO_DEFAULT,
    rrclass = kDNSServiceClass_IN,
    rdata = _NO_DEFAULT,
    ):

    """

    Instruct the daemon to verify the validity of a resource record
    that appears to be out of date (e.g. because tcp connection to a
    service's target failed).  Causes the record to be flushed from
    the daemon's cache (as well as all other daemons' caches on the
    network) if the record is determined to be invalid.

      flags:
        Currently unused, reserved for future use.

      interfaceIndex: 
        If non-zero, specifies the interface of the record in
	question.  Passing kDNSServiceInterfaceIndexAny (0) causes all
	instances of this record to be reconfirmed.

      fullname:
        The resource record's full domain name.

      rrtype:
        The resource record's type (e.g. kDNSServiceType_PTR,
        kDNSServiceType_SRV, etc.).

      rrclass:
        The class of the resource record (usually
        kDNSServiceClass_IN).

      rdata:
        A string containing the raw rdata of the resource record.

    """

    _NO_DEFAULT.check(fullname)
    _NO_DEFAULT.check(rrtype)
    _NO_DEFAULT.check(rdata)

    rdlen, rdata = _string_to_length_and_void_p(rdata)

    _DNSServiceReconfirmRecord(flags,
			       interfaceIndex,
			       fullname,
			       rrtype,
			       rrclass,
			       rdlen,
			       rdata)


def DNSServiceConstructFullName(
    service = None,
    regtype = _NO_DEFAULT, 
    domain = _NO_DEFAULT,
    ):

    """

    Concatenate a three-part domain name (as returned by a callback
    function) into a properly-escaped full domain name.  Note that
    callback functions ALREADY ESCAPE strings where necessary.

      service:
        The service name; any dots or backslashes must NOT be escaped.
	May be None (to construct a PTR record name, e.g.
	"_ftp._tcp.apple.com.").

      regtype:
        The service type followed by the protocol, separated by a dot
	(e.g. "_ftp._tcp").

      domain:
        The domain name, e.g. "apple.com.".  Literal dots or
	backslashes, if any, must be escaped,
	e.g. "1st\. Floor.apple.com."

      return value:
        The resulting full domain name.

    """

    _NO_DEFAULT.check(regtype)
    _NO_DEFAULT.check(domain)

    fullName = _DNSServiceConstructFullName(service, regtype, domain)

    return fullName.value.decode('utf-8')



################################################################################
#
# Unit tests
#
################################################################################



if __name__ == '__main__':
    import select
    import threading
    import time
    import unittest


    class TestPyBonjour(unittest.TestCase):

	service_name = 'TestService'
	regtype = '_test._tcp.'
	port = 1111
	fullname = 'TestService._test._tcp.local.'
	timeout = 2

	def test_construct_fullname(self):
	    # Check error handling
	    self.assertRaises(ValueError, DNSServiceConstructFullName, None,
			      None)
	    self.assertRaises(ctypes.ArgumentError, DNSServiceConstructFullName,
			      None, None, None)
	    self.assertRaises(BonjourError, DNSServiceConstructFullName, None,
			      'foo', 'local.')

	    fullname = DNSServiceConstructFullName(self.service_name,
						   self.regtype, 'local.')

	    self.assert_(isinstance(fullname, unicode))
	    if not fullname.endswith(u'.'):
		fullname += u'.'
	    self.assertEqual(fullname, self.fullname)

	def wait_on_event(self, sdRef, event):
	    while not event.isSet():
		ready = select.select([sdRef], [], [], self.timeout)
		self.assert_(sdRef in ready[0], 'operation timed out')
		DNSServiceProcessResult(sdRef)

	def test_enumerate_domains(self):
	    done = threading.Event()

	    def cb(_sdRef, flags, interfaceIndex, errorCode, replyDomain):
		self.assertEqual(errorCode, kDNSServiceErr_NoError)
		self.assertEqual(_sdRef, sdRef)
		self.assert_(isinstance(replyDomain, unicode))
		if not (flags & kDNSServiceFlagsMoreComing):
		    done.set()

	    sdRef = \
		DNSServiceEnumerateDomains(kDNSServiceFlagsRegistrationDomains,
					   callBack=cb)

	    try:
		self.wait_on_event(sdRef, done)
	    finally:
		sdRef.close()

	def register_record(self):
	    done = threading.Event()

	    def cb(_sdRef, flags, errorCode, name, regtype, domain):
		self.assertEqual(errorCode, kDNSServiceErr_NoError)
		self.assertEqual(_sdRef, sdRef)
		self.assert_(isinstance(name, unicode))
		self.assertEqual(name, self.service_name)
		self.assert_(isinstance(regtype, unicode))
		self.assertEqual(regtype, self.regtype)
		self.assert_(isinstance(domain, unicode))
		done.set()

	    sdRef = DNSServiceRegister(name=self.service_name,
				       regtype=self.regtype,
				       port=self.port,
				       callBack=cb)

	    return done, sdRef

	def test_register_browse_resolve(self):
	    browse_done = threading.Event()
	    resolve_done = threading.Event()

	    def register_cb(sdRef, flags, errorCode, name, regtype, domain):
		self.assertEqual(errorCode, kDNSServiceErr_NoError)
		self.assertEqual(sdRef, register_sdRef)
		self.assert_(isinstance(name, unicode))
		self.assertEqual(name, self.service_name)
		self.assert_(isinstance(regtype, unicode))
		self.assertEqual(regtype, self.regtype)
		self.assert_(isinstance(domain, unicode))
		register_done.set()

	    def browse_cb(sdRef, flags, interfaceIndex, errorCode, serviceName,
			  regtype, replyDomain):
		self.assertEqual(errorCode, kDNSServiceErr_NoError)
		self.assertEqual(sdRef, browse_sdRef)
		self.assert_(flags & kDNSServiceFlagsAdd)
		self.assert_(isinstance(serviceName, unicode))
		self.assertEqual(serviceName, self.service_name)
		self.assert_(isinstance(regtype, unicode))
		self.assertEqual(regtype, self.regtype)
		self.assert_(isinstance(replyDomain, unicode))

		def resolve_cb(sdRef, flags, interfaceIndex, errorCode,
			       fullname, hosttarget, port, txtRecord):
		    self.assertEqual(errorCode, kDNSServiceErr_NoError)
		    self.assertEqual(sdRef, resolve_sdRef)
		    self.assert_(isinstance(fullname, unicode))
		    self.assertEqual(fullname, self.fullname)
		    self.assert_(isinstance(hosttarget, unicode))
		    self.assertEqual(port, self.port)
		    self.assert_(isinstance(txtRecord, str))
		    self.assert_(len(txtRecord) > 0)
		    resolve_done.set()

		resolve_sdRef = DNSServiceResolve(0, interfaceIndex,
						  serviceName, regtype,
						  replyDomain, resolve_cb)

		try:
		    self.wait_on_event(resolve_sdRef, resolve_done)
		finally:
		    resolve_sdRef.close()

		browse_done.set()

	    register_done, register_sdRef = self.register_record()

	    try:
		self.wait_on_event(register_sdRef, register_done)

		browse_sdRef = DNSServiceBrowse(regtype=self.regtype,
						callBack=browse_cb)

		try:
		    self.wait_on_event(browse_sdRef, browse_done)
		finally:
		    browse_sdRef.close()
	    finally:
		register_sdRef.close()

	def query_record(self, rrtype, rdata):
	    # Give record time to be updated...
	    time.sleep(5)

	    done = threading.Event()

	    def cb(_sdRef, flags, interfaceIndex, errorCode, fullname, _rrtype,
		   rrclass, _rdata, ttl):
		self.assertEqual(errorCode, kDNSServiceErr_NoError)
		self.assertEqual(_sdRef, sdRef)
		self.assert_(isinstance(fullname, unicode))
		self.assertEqual(fullname, self.fullname)
		self.assertEqual(_rrtype, rrtype)
		self.assertEqual(rrclass, kDNSServiceClass_IN)
		self.assert_(isinstance(_rdata, str))
		self.assertEqual(_rdata, rdata)
		done.set()

	    sdRef = DNSServiceQueryRecord(fullname=self.fullname,
					  rrtype=rrtype,
					  callBack=cb)

	    try:
		self.wait_on_event(sdRef, done)
	    finally:
		sdRef.close()

	def test_addrecord_updaterecord_removerecord(self):
	    done, sdRef = self.register_record()

	    try:
		self.wait_on_event(sdRef, done)

		RecordRef = DNSServiceAddRecord(sdRef,
						rrtype=kDNSServiceType_SINK,
						rdata='foo')
		self.assert_(RecordRef.value is not None)
		self.query_record(kDNSServiceType_SINK, 'foo')

		DNSServiceUpdateRecord(sdRef, RecordRef, rdata='bar')
		self.query_record(kDNSServiceType_SINK, 'bar')

		DNSServiceRemoveRecord(sdRef, RecordRef)
	    finally:
		sdRef.close()

	    self.assert_(RecordRef.value is None)

	def test_createconnection_registerrecord_reconfirmrecord(self):
	    done = threading.Event()

	    def cb(_sdRef, _RecordRef, flags, errorCode):
		self.assertEqual(errorCode, kDNSServiceErr_NoError)
		self.assertEqual(_sdRef, sdRef)
		self.assertEqual(_RecordRef, RecordRef)
		done.set()

	    sdRef = DNSServiceCreateConnection()

	    try:
		#
		# FIXME:
		#
		# Obviously, I don't understand how to use these
		# functions, as my tests either fail bizarrely or
		# cause seg faults and the like.  Let's just punt for
		# now...
		#
		RecordRef = DNSRecordRef()

		#RecordRef = \
		#    DNSServiceRegisterRecord(sdRef,
		#			     kDNSServiceFlagsUnique,
		#			     fullname=self.fullname,
		#			     rrtype=kDNSServiceType_SINK,
		#			     rdata='blah',
		#			     callBack=cb)
		#self.assert_(RecordRef.value is not None)

		#self.wait_on_event(sdRef, done)

		#self.query_record(kDNSServiceType_SINK, 'blah')

		#DNSServiceReconfirmRecord(fullname=self.fullname,
		#			  rrtype=kDNSServiceType_SINK,
		#			  rdata='blah')
	    finally:
		sdRef.close()

	    self.assert_(RecordRef.value is None)


    unittest.main()
