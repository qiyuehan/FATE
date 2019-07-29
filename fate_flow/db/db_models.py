#
#  Copyright 2019 The FATE Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
import datetime
from arch.api.utils import log_utils
from playhouse.pool import PooledMySQLDatabase
from fate_flow.settings import DATABASE
from arch.api.utils.core import current_timestamp
from peewee import Model, CharField, IntegerField, BigIntegerField, TextField, CompositeKey, BigAutoField
import inspect
import sys

LOGGER = log_utils.getLogger()
data_base_config = DATABASE.copy()
# TODO: create instance according to the engine
engine = data_base_config.pop("engine")
db_name = data_base_config.pop("name")
DB = PooledMySQLDatabase(db_name, **data_base_config)


def close_db(db):
    try:
        if db:
            db.close()
    except Exception as e:
        LOGGER.exception(e)


class DataBaseModel(Model):
    class Meta:
        database = DB

    def to_json(self):
        return self.__dict__['__data__']

    def save(self, *args, **kwargs):
        if hasattr(self, "update_date"):
            self.update_date = datetime.datetime.now()
        if hasattr(self, "update_time"):
            self.update_time = current_timestamp()
        super(DataBaseModel, self).save(*args, **kwargs)


@DB.connection_context()
def init_tables():
    members = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    table_objs = []
    for name, obj in members:
        if obj != DataBaseModel and issubclass(obj, DataBaseModel):
            table_objs.append(obj)
    DB.create_tables(table_objs)


class Job(DataBaseModel):
    f_job_id = CharField(max_length=100)
    f_name = CharField(max_length=500, null=True, default='')
    f_description = TextField(null=True, default='')
    f_tag = CharField(max_length=50, null=True, index=True, default='')
    f_role = CharField(max_length=50, index=True)
    f_party_id = CharField(max_length=50, index=True)
    f_roles = TextField()
    f_initiator_party_id = CharField(max_length=50, index=True, default=-1)
    f_is_initiator = IntegerField(null=True, index=True, default=-1)
    f_dsl = TextField()
    f_runtime_conf = TextField()
    f_run_ip = CharField(max_length=100)
    f_status = CharField(max_length=50)  # waiting/ready/start/running/success/failed/partial/setFailed
    f_current_steps = CharField(max_length=500, null=True)  # record component id in DSL
    f_current_tasks = CharField(max_length=500, null=True)  # record task id
    f_progress = IntegerField(null=True, default=0)
    f_create_time = BigIntegerField()
    f_update_time = BigIntegerField(null=True)
    f_start_time = BigIntegerField(null=True)
    f_end_time = BigIntegerField(null=True)
    f_elapsed = BigIntegerField(null=True)

    class Meta:
        db_table = "t_job"
        primary_key = CompositeKey('f_job_id', 'f_role', 'f_party_id')


class Task(DataBaseModel):
    f_job_id = CharField(max_length=100)
    f_component_name = TextField()
    f_task_id = CharField(max_length=100)
    f_role = CharField(max_length=50, index=True)
    f_party_id = CharField(max_length=50, index=True)
    f_operator = CharField(max_length=100)
    f_run_ip = CharField(max_length=100)
    f_run_pid = IntegerField()
    f_status = CharField(max_length=50)  # running/success/failed
    f_create_time = BigIntegerField()
    f_update_time = BigIntegerField(null=True)
    f_start_time = BigIntegerField(null=True)
    f_end_time = BigIntegerField(null=True)
    f_elapsed = BigIntegerField(null=True)

    class Meta:
        db_table = "t_task"
        primary_key = CompositeKey('f_job_id', 'f_task_id', 'f_role', 'f_party_id')


class MachineLearningModelMeta(DataBaseModel):
    f_id = BigIntegerField(primary_key=True)
    f_role = CharField(max_length=50, index=True)
    f_party_id = CharField(max_length=50, index=True)
    f_roles = TextField()
    f_job_id = CharField(max_length=100)
    f_model_id = CharField(max_length=500, index=True)
    f_model_version = CharField(max_length=500, index=True)
    f_size = BigIntegerField(default=0)
    f_create_time = BigIntegerField(default=0)
    f_update_time = BigIntegerField(default=0)
    f_description = TextField(null=True, default='')
    f_tag = CharField(max_length=50, null=True, index=True, default='')

    class Meta:
        db_table = "t_machine_learning_model_meta"


class TrackingMetric(DataBaseModel):
    _mapper = {}

    @classmethod
    def model(cls, table_index=None, date=None):
        if not table_index:
            table_index = date.strftime(
                '%Y%m%d') if date else datetime.datetime.now().strftime(
                '%Y%m%d')
        class_name = 'TrackingMetric_%s' % table_index

        ModelClass = TrackingMetric._mapper.get(class_name, None)
        if ModelClass is None:

            class Meta:
                db_table = '%s_%s' % ('t_tracking_metric', table_index)

            attrs = {'__module__': cls.__module__, 'Meta': Meta}
            ModelClass = type("%s_%s" % (cls.__name__, table_index), (cls,),
                              attrs)
            TrackingMetric._mapper[class_name] = ModelClass
        return ModelClass()

    f_id = BigAutoField(primary_key=True)
    f_job_id = CharField(max_length=100)
    f_component_name = TextField()
    f_task_id = CharField(max_length=100)
    f_role = CharField(max_length=50, index=True)
    f_party_id = CharField(max_length=50, index=True)
    f_metric_namespace = CharField(max_length=200, index=True)
    f_metric_name = CharField(max_length=500, index=True)
    f_key = CharField(max_length=200)
    f_value = TextField()
    f_type = IntegerField(index=True)  # 0 is data, 1 is meta
    f_create_time = BigIntegerField()
    f_update_time = BigIntegerField(null=True)


init_tables()