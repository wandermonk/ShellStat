import os

from typing import Optional
from rocksdict import Rdict, Options, SliceTransform, PlainTableFactoryOptions

def db_options():
    opt = Options()
    # create table
    opt.create_if_missing(True)
    # config to more jobs
    opt.set_max_background_jobs(os.cpu_count() or 1)
    # configure mem-table to a large value (256 MB)
    opt.set_write_buffer_size(0x10000000)
    opt.set_level_zero_file_num_compaction_trigger(4)
    # configure l0 and l1 size, let them have the same size (1 GB)
    opt.set_max_bytes_for_level_base(0x40000000)
    # 256 MB file size
    opt.set_target_file_size_base(0x10000000)
    # use a smaller compaction multiplier
    opt.set_max_bytes_for_level_multiplier(4.0)
    # use 8-byte prefix (2 ^ 64 is far enough for transaction counts)
    opt.set_prefix_extractor(SliceTransform.create_max_len_prefix(8))
    # set to plain-table
    opt.set_plain_table_factory(PlainTableFactoryOptions())
    return opt


class RocksDBConnection:
    _instance: Optional['RocksDBConnection'] = None
    db: Rdict

    def __new__(cls, db_path: str) -> 'RocksDBConnection':
        if cls._instance is None:
            cls._instance = super(RocksDBConnection, cls).__new__(cls)
            cls._instance.db = Rdict(os.path.join(os.path.dirname(db_path), '.metrics_db'), db_options())
        return cls._instance
    
    @staticmethod
    def get_instance(db_path: str) -> 'Rdict':
        if RocksDBConnection._instance is None:
            raise ValueError("DB not initialized or not of type Rdict")
        return RocksDBConnection._instance.db

    @staticmethod
    def destroy():
        if RocksDBConnection._instance and hasattr(RocksDBConnection._instance, "db"):
            RocksDBConnection._instance.db.close()
            RocksDBConnection._instance = None