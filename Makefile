STAGES := bplrt ewl_expo dover ewl_changi_airport sklrt_east_loop \
nel pglrt_east_loop_and_sklrt_west_loop buangkok oasis farmway ewl_boon_lay_extension \
ccl_3 ccl_1_and_ccl_2 ten_mile_junction_temporary_closure woodleigh_and_damai \
ccl_4_and_ccl_5 ten_mile_junction_reopen ccl_e cheng_lim dtl_1 pglrt_west_loop \
marina_south_pier kupang dtl_2 sam_kee punggol_point samudera ewl_tuas_extension \
dtl_3 ten_mile_junction_permanent_closure canberra tel_1 tel_2 tel_3 tel_4 \
punggol_coast_extension teck_lee hume \
tel_5_and_dtl_3e ccl_6 jrl_1 founders_memorial \
jrl_2 jrl_3 crl_1 crl_2 crl_pe brickland cg_tel_c future

generate_all:
	@for stage in $(STAGES); do \
		echo "Generating config file for stage: $$stage"; \
		poetry run python railrailrail/cli.py --generate-config --network $$stage; \
	done
