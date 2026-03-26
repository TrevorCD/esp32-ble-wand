.PHONY: app
.SILENT: app

all: app stm32

app:
	python3.14 app/app.py

stm32:
	$(MAKE) -C stm32

stm-flash: stm32
	st-flash write stm32/build/stm32.bin 0x8000000

ocd:
	openocd -f openocd.cfg

gdb:
	arm-none-eabi-gdb stm32/build/stm32.elf
