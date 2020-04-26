This fork adds support for dwire-debug uploads. Make sure the fuses are set to allow upload via dwdebug.
This normally implies the following atleast be enabled:

* DWEN
* SELFPRGEN
* RSTDISBL (not sure)

To enable debug via PlatformIO's Unified Platform, set `upload_protocol`, 
`debug_tool`, `debug_port`, `debug_server` and `debug_init_cmds` as below:

```
[env:attiny85]
platform = https://github.com/faisyl/platform-atmelavr.git
board = attiny85
framework = arduino

upload_protocol = dwdebug
debug_tool = custom
debug_port = :4444
debug_server = 
  $PLATFORMIO_CORE_DIR/packages/tool-dwdebug/dwdebug 
  verbose,gdbserver

debug_init_cmds =
  target remote localhost:4444
  set remoteaddresssize 32
```

