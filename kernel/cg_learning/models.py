import abc
import datetime
import json
from collections import OrderedDict
from enum import Enum

import pytz


class JsonSerializable:
    @abc.abstractmethod
    def to_dict(self):
        pass

    def __str__(self):
        return json.dumps(self.to_dict(), sort_keys=False, ensure_ascii=False)


class Verb(JsonSerializable):

    def __init__(self, verb_id: str=None, meaning_zh: str=None):
        self.verb_id = verb_id
        self.display = None
        if meaning_zh is not None:
            self.display = {"zh": meaning_zh}

    def to_dict(self):
        ret = OrderedDict()
        if self.verb_id:
            ret['id'] = self.verb_id
        if self.display:
            ret['display'] = self.display
        return ret


class Actor(JsonSerializable):
    class ObjectType(Enum):
        AGENT = "Agent"
        GROUP = "Group"

    class Account:
        def __init__(self, home_page, name):
            self.home_page = home_page
            self.name = name

    def __init__(self, account: Account,
                 object_type: ObjectType=ObjectType.AGENT,
                 mail_box: str=None,
                 openid: str=None,
                 member=None,
                 ):
        self.object_type = object_type
        self._mbox_sha1sum = None
        self._mbox = None
        self.mbox = mail_box
        self.openid = openid
        self.member = member
        self.account = account

    @property
    def mbox_sha1sum(self):
        return self._mbox_sha1sum

    @property
    def mbox(self):
        return self._mbox

    @mbox.setter
    def mbox(self, value):
        pass

    def to_dict(self):
        ret = OrderedDict()
        if self.mbox:
            ret['mbox'] = self.mbox
        if self.mbox_sha1sum:
            ret['mbox_sha1sum'] = self.mbox_sha1sum
        if self.openid:
            ret['openid'] = self.openid
        if self.account.name:
            ret['account'] = OrderedDict()
            ret['account']['name'] = self.account.name
            ret['account']['homePage'] = self.account.home_page
        if self.object_type == 'Group':
            # show members for groups if ids_only is false
            # show members' ids for anon groups if ids_only is true
            if not ({'mbox', 'mbox_sha1sum', 'openid', 'account'} & set(ret.keys())):
                if self.member.all():
                    ret['member'] = [a.to_dict() for a in self.member.all()]

        ret['objectType'] = self.object_type.value
        return ret


class Activity(JsonSerializable):

    def __init__(self, activity_id: str, name: str=None,
                 activity_type: str=None, description: dict=None):
        self.activity_id = activity_id
        self.name = name
        self.description = description
        self.type = activity_type
        self.extensions = None

    def to_dict(self):
        ret = OrderedDict()
        ret["id"] = self.activity_id
        ret["objectType"] = "Activity"
        if self.name:
            ret["name"] = self.name
        if self.description:
            ret["description"] = self.description
        if self.type:
            ret["type"] = self.type
        if self.extensions:
            ret["extensions"] = self.extensions
        return ret


class Statement(JsonSerializable):
    class ContextActivityType(Enum):
        Parent = "parent"
        Grouping = "grouping"
        Category = "category"
        Other = "other"

    def __init__(self, actor: Actor, verb: Verb, statement_id: str=None):
        # If no statement_id is given, will create one automatically
        import uuid
        self.statement_id = uuid.uuid4() if statement_id is None else statement_id
        self.actor = actor
        self.verb = verb
        self.object_activity = None
        self.object_substatement = None
        self.object_statementref = None
        self.result_success = None
        self.result_completion = None
        self.result_response = None
        self.result_duration = None         # ms
        self.result_score_scaled = None
        self.result_score_raw = None
        self.result_score_min = None
        self.result_score_max = None
        self.result_extensions = None
        self._timestamp = None
        self.update_timestamp()
        self.context_registration = None
        self.context_instructor = None
        self.context_team = None
        self.context_revision = None
        self.context_platform = None
        self.context_language = None
        self.context_extensions = None
        self._context_ca = None
        self.context_statement_id = None
        self._attachments = None

    def update_timestamp(self):
        timezone = pytz.timezone('Asia/Shanghai')
        self._timestamp = datetime.datetime.now(timezone).isoformat(timespec='milliseconds')

    def add_result_extension(self, key: str, value):
        if key is None or value is None:
            return
        self.update_result_extensions({key: value}, True)

    def update_result_extensions(self, extensions: dict, smart_update=False):
        if extensions is None or not extensions:
            return
        if self.result_extensions is None:
            self.result_extensions = {}
        # simple update when smart_update=False or result_score_raw field is already set
        if not smart_update or self.result_score_raw is not None:
            self.result_extensions.update(extensions)
            return
        # find potential key present score
        # deep copy prevent from modifying original case result
        import copy
        extensions_copy = copy.deepcopy(extensions)
        score = None
        for key in extensions_copy.keys():
            if 'score' == key.lower():
                score = extensions_copy[key]
                del extensions_copy[key]
                break
        if score:
            self.result_score_raw = score
        self.update_result_extensions(extensions_copy, False)

    def add_attachment(self, sha_code, file_path: str,
                       usage_type: str=None, description: dict=None):
        if self._attachments is None:
            self._attachments = {}
        self._attachments[sha_code] = {
            "path": file_path,
            "type": usage_type,
            "description": description
        }

    def add_context_activity(self, ca_type: ContextActivityType, activity_id: str):
        if self._context_ca is None:
            self._context_ca = {}
        if ca_type not in self._context_ca.keys():
            self._context_ca[ca_type] = set()
        self._context_ca[ca_type].add(activity_id)

    def add_context_extensions(self, key, value):
        if self.context_extensions is None:
            self.context_extensions = {}
        self.context_extensions[key] = value

    def get_attachments(self):
        return self._attachments

    def to_dict(self):
        ret = OrderedDict()

        ret['id'] = str(self.statement_id)
        ret['actor'] = self.actor.to_dict()
        ret['verb'] = self.verb.to_dict()

        if self.object_activity:
            ret['object'] = self.object_activity.to_dict()
        elif self.object_substatement:
            ret['object'] = self.object_substatement.to_dict()
        else:
            ret['object'] = {
                'id': str(self.object_statementref), 'objectType': 'StatementRef'}

        ret['result'] = OrderedDict()
        if self.result_success is not None:
            ret['result']['success'] = self.result_success
        if self.result_completion is not None:
            ret['result']['completion'] = self.result_completion
        if self.result_response:
            ret['result']['response'] = self.result_response
        if self.result_duration:
            ret['result']['duration'] = int(self.result_duration)

        ret['result']['score'] = OrderedDict()
        if self.result_score_scaled is not None:
            ret['result']['score']['scaled'] = self.result_score_scaled
        if self.result_score_raw is not None:
            ret['result']['score']['raw'] = self.result_score_raw
        if self.result_score_min is not None:
            ret['result']['score']['min'] = self.result_score_min
        if self.result_score_max is not None:
            ret['result']['score']['max'] = self.result_score_max
        # If there is no score, delete from dict
        if not ret['result']['score']:
            del ret['result']['score']
        if self.result_extensions:
            ret['result']['extensions'] = self.result_extensions
        if not ret['result']:
            del ret['result']

        ret['context'] = OrderedDict()
        if self.context_registration:
            ret['context']['registration'] = self.context_registration
        if self.context_instructor:
            ret['context'][
                'instructor'] = self.context_instructor.to_dict()
        if self.context_team:
            ret['context']['team'] = self.context_team.to_dict()
        if self.context_revision:
            ret['context']['revision'] = self.context_revision
        if self.context_platform:
            ret['context']['platform'] = self.context_platform
        if self.context_language:
            ret['context']['language'] = self.context_language
        if self.context_statement_id:
            ret['context']['statement'] = {
                'id': self.context_statement_id, 'objectType': 'StatementRef'}

        ret['context']['contextActivities'] = OrderedDict()
        if self._context_ca:
            for ca_type in [Statement.ContextActivityType.Parent,
                            Statement.ContextActivityType.Grouping,
                            Statement.ContextActivityType.Category,
                            Statement.ContextActivityType.Other]:
                if ca_type in self._context_ca.keys():
                    ret['context']['contextActivities'][ca_type.value] = list(self._context_ca[ca_type])
        if self.context_extensions:
            ret['context']['extensions'] = self.context_extensions
        if not ret['context']['contextActivities']:
            del ret['context']['contextActivities']
        if not ret['context']:
            del ret['context']

        if self._attachments:
            ret["attachments"] = []
            for sha in self._attachments:
                attachment = self._attachments[sha]
                ret["attachments"].append({"sha2": sha, "usageType": attachment["type"],
                                           "description": attachment["description"]})
        ret['timestamp'] = self._timestamp
        return ret
