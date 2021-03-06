# -*- encoding: utf-8
# yapf: disable


checkname = 'mongodb_collections'


info = [[u'unshardedDB2', u'collections1', u'count', u'3000'],
        [u'unshardedDB2', u'collections1', u'storageSize', u'61440'],
        [u'unshardedDB2', u'collections1', u'ok', u'1.0'],
        [u'unshardedDB2', u'collections1', u'avgObjSize', u'34.0'],
        [u'unshardedDB2', u'collections1', u'shardsCount', u'1'],
        [u'unshardedDB2', u'collections1', u'nchunks', u'1'],
        [u'unshardedDB2', u'collections1', u'primary', u'shard02'],
        [u'unshardedDB2', u'collections1', u'totalIndexSize', u'40960'],
        [u'unshardedDB2', u'collections1', u'maxSize', u'0'],
        [u'unshardedDB2', u'collections1', u'sharded', u'False'],
        [u'unshardedDB2', u'collections1', u'capped', u'False'],
        [u'unshardedDB2', u'collections1', u'nindexes', u'1'],
        [u'unshardedDB2', u'collections1', u'ns', u'unshardedDB2.collections1'],
        [u'unshardedDB2', u'collections1', u'size', u'102000'],
        [u'unshardedDB2', u'collections2', u'count', u'666'],
        [u'unshardedDB2', u'collections2', u'storageSize', u'24576'],
        [u'unshardedDB2', u'collections2', u'ok', u'1.0'],
        [u'unshardedDB2', u'collections2', u'avgObjSize', u'36.0'],
        [u'unshardedDB2', u'collections2', u'shardsCount', u'1'],
        [u'unshardedDB2', u'collections2', u'nchunks', u'1'],
        [u'unshardedDB2', u'collections2', u'primary', u'shard02'],
        [u'unshardedDB2', u'collections2', u'totalIndexSize', u'20480'],
        [u'unshardedDB2', u'collections2', u'maxSize', u'0'],
        [u'unshardedDB2', u'collections2', u'sharded', u'False'],
        [u'unshardedDB2', u'collections2', u'capped', u'False'],
        [u'unshardedDB2', u'collections2', u'nindexes', u'1'],
        [u'unshardedDB2', u'collections2', u'ns', u'unshardedDB2.collections2'],
        [u'unshardedDB2', u'collections2', u'size', u'23976'],
        [u'shardedDB1', u'collections1', u'count', u'10000'],
        [u'shardedDB1', u'collections1', u'storageSize', u'409600'],
        [u'shardedDB1', u'collections1', u'ok', u'1.0'],
        [u'shardedDB1', u'collections1', u'avgObjSize', u'40.0'],
        [u'shardedDB1', u'collections1', u'dropped', u'False'],
        [u'shardedDB1', u'collections1', u'unique', u'False'],
        [u'shardedDB1', u'collections1', u'nchunks', u'6'],
        [u'shardedDB1', u'collections1', u'shardsCount', u'3'],
        [u'shardedDB1', u'collections1', u'totalIndexSize', u'622592'],
        [u'shardedDB1', u'collections1', u'maxSize', u'0'],
        [u'shardedDB1', u'collections1', u'sharded', u'True'],
        [u'shardedDB1', u'collections1', u'capped', u'False'],
        [u'shardedDB1', u'collections1', u'nindexes', u'2'],
        [u'shardedDB1', u'collections1', u'ns', u'shardedDB1.collections1'],
        [u'shardedDB1', u'collections1', u'size', u'407470'],
        [u'shardedDB1', u'collections2', u'count', u'10000'],
        [u'shardedDB1', u'collections2', u'storageSize', u'290816'],
        [u'shardedDB1', u'collections2', u'ok', u'1.0'],
        [u'shardedDB1', u'collections2', u'avgObjSize', u'39.0'],
        [u'shardedDB1', u'collections2', u'dropped', u'False'],
        [u'shardedDB1', u'collections2', u'unique', u'False'],
        [u'shardedDB1', u'collections2', u'nchunks', u'6'],
        [u'shardedDB1', u'collections2', u'shardsCount', u'3'],
        [u'shardedDB1', u'collections2', u'totalIndexSize', u'339968'],
        [u'shardedDB1', u'collections2', u'maxSize', u'0'],
        [u'shardedDB1', u'collections2', u'sharded', u'True'],
        [u'shardedDB1', u'collections2', u'capped', u'False'],
        [u'shardedDB1', u'collections2', u'nindexes', u'2'],
        [u'shardedDB1', u'collections2', u'ns', u'shardedDB1.collections2'],
        [u'shardedDB1', u'collections2', u'size', u'399913'],
        [u'shardedDB2', u'collections2', u'count', u'100000'],
        [u'shardedDB2', u'collections2', u'storageSize', u'2744320'],
        [u'shardedDB2', u'collections2', u'ok', u'1.0'],
        [u'shardedDB2', u'collections2', u'avgObjSize', u'40.0'],
        [u'shardedDB2', u'collections2', u'dropped', u'False'],
        [u'shardedDB2', u'collections2', u'unique', u'False'],
        [u'shardedDB2', u'collections2', u'nchunks', u'6'],
        [u'shardedDB2', u'collections2', u'shardsCount', u'3'],
        [u'shardedDB2', u'collections2', u'totalIndexSize', u'4104192'],
        [u'shardedDB2', u'collections2', u'maxSize', u'0'],
        [u'shardedDB2', u'collections2', u'sharded', u'True'],
        [u'shardedDB2', u'collections2', u'capped', u'False'],
        [u'shardedDB2', u'collections2', u'nindexes', u'2'],
        [u'shardedDB2', u'collections2', u'ns', u'shardedDB2.collections2'],
        [u'shardedDB2', u'collections2', u'size', u'4074785'],
        [u'unshardedDB1', u'collections1', u'count', u'1000'],
        [u'unshardedDB1', u'collections1', u'storageSize', u'32768'],
        [u'unshardedDB1', u'collections1', u'ok', u'1.0'],
        [u'unshardedDB1', u'collections1', u'avgObjSize', u'35.0'],
        [u'unshardedDB1', u'collections1', u'shardsCount', u'1'],
        [u'unshardedDB1', u'collections1', u'nchunks', u'1'],
        [u'unshardedDB1', u'collections1', u'primary', u'shard03'],
        [u'unshardedDB1', u'collections1', u'totalIndexSize', u'20480'],
        [u'unshardedDB1', u'collections1', u'maxSize', u'0'],
        [u'unshardedDB1', u'collections1', u'sharded', u'False'],
        [u'unshardedDB1', u'collections1', u'capped', u'False'],
        [u'unshardedDB1', u'collections1', u'nindexes', u'1'],
        [u'unshardedDB1', u'collections1', u'ns', u'unshardedDB1.collections1'],
        [u'unshardedDB1', u'collections1', u'size', u'35000'],
        [u'jumboDB1', u'collections1', u'count', u'0'],
        [u'jumboDB1', u'collections1', u'storageSize', u'12288'],
        [u'jumboDB1', u'collections1', u'ok', u'1.0'],
        [u'jumboDB1', u'collections1', u'avgObjSize', u'0.0'],
        [u'jumboDB1', u'collections1', u'dropped', u'False'],
        [u'jumboDB1', u'collections1', u'unique', u'False'],
        [u'jumboDB1', u'collections1', u'nchunks', u'6'],
        [u'jumboDB1', u'collections1', u'shardsCount', u'3'],
        [u'jumboDB1', u'collections1', u'totalIndexSize', u'24576'],
        [u'jumboDB1', u'collections1', u'maxSize', u'0'],
        [u'jumboDB1', u'collections1', u'sharded', u'True'],
        [u'jumboDB1', u'collections1', u'capped', u'False'],
        [u'jumboDB1', u'collections1', u'nindexes', u'2'],
        [u'jumboDB1', u'collections1', u'ns', u'jumboDB1.collections1'],
        [u'jumboDB1', u'collections1', u'size', u'0']]


discovery = {'': [(u'jumboDB1 collections1', {}),
                  (u'shardedDB1 collections1', {}),
                  (u'shardedDB1 collections2', {}),
                  (u'shardedDB2 collections2', {}),
                  (u'unshardedDB1 collections1', {}),
                  (u'unshardedDB2 collections1', {}),
                  (u'unshardedDB2 collections2', {})]}


checks = {'': [(u'jumboDB1 collections1',
                {},
                [(0,
                  'Uncompressed size in memory: 0.00 B',
                  [('mongodb_collection_size', 0, None, None, None, None)]),
                 (0,
                  'Allocated for document storage: 12.00 kB',
                  [('mongodb_collection_storage_size',
                    12288,
                    None,
                    None,
                    None,
                    None)]),
                 (0,
                  u'\nCollection\n- Sharded: True (Data distributed in cluster)\n- Shards: 3 (Number of shards)\n- Chunks: 6 (Total number of chunks)\n- Document Count: 0 (Number of documents in collection)\n- Object Size 0.00 B (Average object size)\n- Collection Size: 0.00 B (Uncompressed size in memory)\n- Storage Size: 12.00 kB (Allocated for document storage)',
                  [])]),
               (u'shardedDB1 collections1',
                {},
                [(0,
                  'Uncompressed size in memory: 397.92 kB',
                  [('mongodb_collection_size', 407470, None, None, None, None)]),
                 (0,
                  'Allocated for document storage: 400.00 kB',
                  [('mongodb_collection_storage_size',
                    409600,
                    None,
                    None,
                    None,
                    None)]),
                 (0,
                  u'\nCollection\n- Sharded: True (Data distributed in cluster)\n- Shards: 3 (Number of shards)\n- Chunks: 6 (Total number of chunks)\n- Document Count: 10000 (Number of documents in collection)\n- Object Size 40.00 B (Average object size)\n- Collection Size: 397.92 kB (Uncompressed size in memory)\n- Storage Size: 400.00 kB (Allocated for document storage)',
                  [])]),
               (u'shardedDB1 collections2',
                {},
                [(0,
                  'Uncompressed size in memory: 390.54 kB',
                  [('mongodb_collection_size', 399913, None, None, None, None)]),
                 (0,
                  'Allocated for document storage: 284.00 kB',
                  [('mongodb_collection_storage_size',
                    290816,
                    None,
                    None,
                    None,
                    None)]),
                 (0,
                  u'\nCollection\n- Sharded: True (Data distributed in cluster)\n- Shards: 3 (Number of shards)\n- Chunks: 6 (Total number of chunks)\n- Document Count: 10000 (Number of documents in collection)\n- Object Size 39.00 B (Average object size)\n- Collection Size: 390.54 kB (Uncompressed size in memory)\n- Storage Size: 284.00 kB (Allocated for document storage)',
                  [])]),
               (u'shardedDB2 collections2',
                {},
                [(0,
                  'Uncompressed size in memory: 3.89 MB',
                  [('mongodb_collection_size', 4074785, None, None, None, None)]),
                 (0,
                  'Allocated for document storage: 2.62 MB',
                  [('mongodb_collection_storage_size',
                    2744320,
                    None,
                    None,
                    None,
                    None)]),
                 (0,
                  u'\nCollection\n- Sharded: True (Data distributed in cluster)\n- Shards: 3 (Number of shards)\n- Chunks: 6 (Total number of chunks)\n- Document Count: 100000 (Number of documents in collection)\n- Object Size 40.00 B (Average object size)\n- Collection Size: 3.89 MB (Uncompressed size in memory)\n- Storage Size: 2.62 MB (Allocated for document storage)',
                  [])]),
               (u'unshardedDB1 collections1',
                {},
                [(0,
                  'Uncompressed size in memory: 34.18 kB',
                  [('mongodb_collection_size', 35000, None, None, None, None)]),
                 (0,
                  'Allocated for document storage: 32.00 kB',
                  [('mongodb_collection_storage_size',
                    32768,
                    None,
                    None,
                    None,
                    None)]),
                 (0,
                  u'\nCollection\n- Sharded: False (Data distributed in cluster)\n- Shards: 1 (Number of shards)\n- Chunks: 1 (Total number of chunks)\n- Document Count: 1000 (Number of documents in collection)\n- Object Size 35.00 B (Average object size)\n- Collection Size: 34.18 kB (Uncompressed size in memory)\n- Storage Size: 32.00 kB (Allocated for document storage)',
                  [])]),
               (u'unshardedDB2 collections1',
                {},
                [(0,
                  'Uncompressed size in memory: 99.61 kB',
                  [('mongodb_collection_size', 102000, None, None, None, None)]),
                 (0,
                  'Allocated for document storage: 60.00 kB',
                  [('mongodb_collection_storage_size',
                    61440,
                    None,
                    None,
                    None,
                    None)]),
                 (0,
                  u'\nCollection\n- Sharded: False (Data distributed in cluster)\n- Shards: 1 (Number of shards)\n- Chunks: 1 (Total number of chunks)\n- Document Count: 3000 (Number of documents in collection)\n- Object Size 34.00 B (Average object size)\n- Collection Size: 99.61 kB (Uncompressed size in memory)\n- Storage Size: 60.00 kB (Allocated for document storage)',
                  [])]),
               (u'unshardedDB2 collections2',
                {},
                [(0,
                  'Uncompressed size in memory: 23.41 kB',
                  [('mongodb_collection_size', 23976, None, None, None, None)]),
                 (0,
                  'Allocated for document storage: 24.00 kB',
                  [('mongodb_collection_storage_size',
                    24576,
                    None,
                    None,
                    None,
                    None)]),
                 (0,
                  u'\nCollection\n- Sharded: False (Data distributed in cluster)\n- Shards: 1 (Number of shards)\n- Chunks: 1 (Total number of chunks)\n- Document Count: 666 (Number of documents in collection)\n- Object Size 36.00 B (Average object size)\n- Collection Size: 23.41 kB (Uncompressed size in memory)\n- Storage Size: 24.00 kB (Allocated for document storage)',
                  [])])]}