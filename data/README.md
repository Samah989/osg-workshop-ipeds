# Sample data for the workshop

This folder should contain **5 parquet files**, one per IPEDS dataset for 2015:

- `directory__2015__all__57e89e4ac1.parquet`  (~2 MB  -  institution directory)
- `finance__2015__all__97ccbf3c00.parquet`  (~4 MB  -  finance)
- `grad-rates__2015__all__126adec85d.parquet`  (~2 MB  -  graduation rates)
- `grad-rates-pell__2015__all__96245aa82c.parquet`  (~600 KB  -  Pell grad rates)
- `sfa-all-undergraduates__2015__all__3ee2bc4b24.parquet`  (~450 KB  -  student financial aid)

**Total size: ~10 MB.**

## Populate this folder

If your OSG account has the full 75-parquet dataset from an earlier pull, copy the 2015 files here:

```bash
# on ap40, from ~/workshop
cp ~/ipeds-analysis/osg/data/directory__2015__* data/
cp ~/ipeds-analysis/osg/data/finance__2015__* data/
cp ~/ipeds-analysis/osg/data/grad-rates__2015__* data/
cp ~/ipeds-analysis/osg/data/grad-rates-pell__2015__* data/
cp ~/ipeds-analysis/osg/data/sfa-all-undergraduates__2015__* data/
```

Otherwise pull them from the Urban Institute Education Data Portal API using the pattern shown in the `pull_all_panels.py` script from the main IPEDS project.

Data source: [Urban Institute Education Data Portal](https://educationdata.urban.org/documentation/)  -  public IPEDS data, no auth needed.
