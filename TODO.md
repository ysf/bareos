## Introduction

The "configure add" command is able to create bareos resources and store
them into the configuration directory.

configure add storage password=foo address=bar.tld device=file mediatype=file name=test0
Created resource config file "/etc/bareos/bareos-dir.d/storage/test0.conf":
Storage {
  Password = foo
  Address = bar.tld
  Device = file
  MediaType = file
  Name = test0
}

##  Problem description

When a string with whitespace needs to be added, the string is written without quotes into the configuration file.
(In this example the "description" filed)

configure add storage password=foo address=bar.tld device=file mediatype=file name=test0 description="string with whitespace"
Created resource config file "/etc/bareos/bareos-dir.d/storage/test0.conf":
Storage {
  Password = foo
  Address = bar.tld
  Device = file
  MediaType = file
  Name = test0
  Description = string with whitespace
}



The correct way would be:

  Description = "string with whitespace"


