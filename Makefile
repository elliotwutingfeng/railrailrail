STAGES := now punggol_coast_extension teck_lee hume \
tel_5_and_dtl_3e ccl_6 jrl_1 founders_memorial \
jrl_2 jrl_3 crl_1 crl_2 crl_pe brickland cg_tel_c future

generate_all:
	@for stage in $(STAGES); do \
		echo "Generating config file for stage: $$stage"; \
		poetry run python railrailrail/cli.py --generate-config --network $$stage; \
	done
