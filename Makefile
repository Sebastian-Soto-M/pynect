COVERAGE=coverage run -m --branch tests

.PHONY:
	test
	test-utils
	report
	html-report

test:
	$(COVERAGE)

test-utils:
	coverage run -m --branch

report:
	@test
	$(COVERAGE).utils
