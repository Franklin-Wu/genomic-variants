from django.db import models

# Create your models here.
class Genes(models.Model):
    name    = models.CharField('Gene', max_length=128)
    nchange = models.CharField('Nucleotide Change', max_length=2048)
    pchange = models.CharField('Protein Change', max_length=2048)
    maps    = models.CharField('Other Mappings', max_length=2048)
    alias   = models.CharField('Alias', max_length=2048)
    trans   = models.CharField('Transcripts', max_length=2048)
    region  = models.CharField('Region', max_length=2048)
    rclass  = models.CharField('Reported Classification', max_length=2048)
    iclass  = models.CharField('Inferred Classification', max_length=2048)
    source  = models.CharField('Source', max_length=2048)
    leval   = models.CharField('Last Evaluated', max_length=2048)
    lupdate = models.CharField('Last Updated', max_length=2048)
    url     = models.CharField('URL', max_length=2048)
    comment = models.CharField('Submitter Comment', max_length=8192)
