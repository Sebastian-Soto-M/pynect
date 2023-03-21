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
	coverage report --skip-covered --sort Miss

html-report:
	@report
	coverage html --skip-empty --title "Pynect Tests"
