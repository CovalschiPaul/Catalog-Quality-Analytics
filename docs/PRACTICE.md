# Exercises and interview preparation

Work without looking at the solution first, then compare with the numbered analysis files.

1. Count listings by category and marketplace. Add a WHERE clause for DE.
2. Find NULL and whitespace-only titles. Why does `title = NULL` fail?
3. LEFT JOIN checks to issues. Show why COUNT(*) gives the wrong affected-check denominator.
4. Calculate category failure rates, keeping checks without issues.
5. Find invalid parent references; why must marketplace be part of the join?
6. Reconstruct May-end backlog. Why does filtering only today's NULL closures undercount historical backlog?
7. Rank marketplace backlog contributions. Explain the denominator of each percentage.
8. Preview duplicate retention using ROW_NUMBER. Add a deterministic tie-breaker.
9. Explain why LAG gives a blank value for the first month.
10. Independent extension: add a query for average resolution time among closed issues, and explain why it excludes unresolved tickets and may favour faster cases. SQLite and PostgreSQL date arithmetic differ; write and validate the version for your chosen engine.

## Readiness check

Be able to change an as-of date, add a marketplace filter, explain join cardinality and debug a total that differs from Power BI. Explain which patterns were planted in the synthetic data. State what additional evidence you would need before making a business recommendation.

## Honest interview narrative

Explain the operational problem, the table grains, the denominator choice, the historical backlog logic, and one bug a boundary test prevents. Explain which parts you wrote or changed yourself and how AI assisted. Do not claim this scaffold was deployed at Amazon or saved a company money.
