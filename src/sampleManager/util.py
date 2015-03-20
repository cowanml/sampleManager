import uuid


# this seems backwards?
#def new_uid(uid=None, db=None, collection=None):
#    """
#    if uid=None, get a new, unused uuid.
#    if uid is defined and exists in the collection, return uuid.
#    if uid is defined and doesn't exist in the collection, raise error.
#    """
#    
#    if(isinstance(uid, uuid.UUID)):
#        return uid
#
#    elif(uid is None):
#        while(True):
#            
#            break
#        return uid


def new_uid(alias=None, s=None):
    """
    if uid==None, get a new, unused uuid.
    """
    
#    objs = s.__class__.objects()

#    while(True):
    try_uid = str(uuid.uuid4())
 #       if try_uid not in [obj.uid for obj in objs.only('uid')]:
#    if try_uid not in [obj.uid for obj in s.only('uid')]:
#    if try_uid not in [obj.uid for obj in s]:
#    print [o.uid for o in s]
    print "it's unique!"
#        break

    return try_uid
