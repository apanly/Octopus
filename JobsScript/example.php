#!/usr/bin/php

<?php

<<<EOT
这个程序模拟PHPJOB运行的典型流程
EOT;

print "example for php\n";

print "START\n";
sleep(1);

//read cursor 
$options=getopt("f:");
$cur=(int)@file_get_contents($options['f']);

for ($i=0;$i<=$cur;$i++)
{
        print "HEARTBEAT\n";
        sleep(1);
}

//write cursor
@file_put_contents($i);

sleep(1);
print "END\n";
