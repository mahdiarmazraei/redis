# redis
create redis with python
It has the mentioned commands (get, set, ttl, delete, expire)
Has additional command commands and keys
The ability to recover data using a json file, that is, when the program is closed and reopened, the data will be saved, even if the data is in the expire state, the time will be calculated. I wrote it with a json file so that it would be easier to run, otherwise it could be run with a postgresql database.
It has the ability of synchronicity.
It has error management.
You can query several terminals at the same time
