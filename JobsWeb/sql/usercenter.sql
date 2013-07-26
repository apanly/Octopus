use jobs_db;

create table if not exists ajk_admin_manager(
    `MId` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `UserName` varchar(50) NOT NULL,
    `UserPasswd` varchar(50) NOT NULL
)
;

truncate table ajk_admin_manager;

insert into ajk_admin_manager(username, userpasswd)
values('root', 'ZTEwYWRjMzk0OWjhNTlhYmjlNTZlMDU3ZjIwZjg4M2U=');
