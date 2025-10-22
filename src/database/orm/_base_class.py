from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from datetime import datetime


metadata_obj = MetaData(schema="public")


class Base(DeclarativeBase):
    metadata = metadata_obj

    def as_dict(
        self, transform_dates: bool = False, fields_to_exclude: list[str] = None
    ) -> dict:
        temp_dict = self.__dict__
        try:
            del temp_dict["_sa_instance_state"]
        except Exception:
            ...

        if fields_to_exclude:
            for field_name in fields_to_exclude:
                try:
                    del temp_dict[field_name]
                except Exception:
                    ...

        if transform_dates:
            temp_dict = {
                key: (value.timestamp() if isinstance(value, datetime) else value)
                for key, value in temp_dict.items()
            }

        return temp_dict
