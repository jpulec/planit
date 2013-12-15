from django.shortcuts import redirect

from social.pipeline.partial import partial

import logging

from niteabout.apps.main.models import UserProfile

logger = logging.getLogger(__name__)

@partial
def require_profile(strategy, details, user=None, is_new=False, *args, **kwargs):
    logger.info(is_new)
    logger.info(kwargs)
    if user and hasattr(user, "userprofile") and user.userprofile:
        return
    elif is_new:
        if strategy.session_get('saved_profile'):
            return {'userprofile': strategy.session_pop('saved_profile'),
                    'user': user,
                    'is_new': is_new}
        else:
            return redirect('require_profile')

def associate_profile(strategy, user, userprofile, is_new=False, *args, **kwargs):
    if user and hasattr(user, "userprofile") and user.userprofile:
        return
    else:
        profile = UserProfile.objects.create(auth=user, **userprofile)


def check_if_niteabout(strategy, request, user, args, **kwargs):
    if strategy.session_get('niteabout'):
        niteabout = strategy.session_pop('niteabout')
        logger.info(niteabout)
        #niteabout.attendees.add(user.userprofile)
