import pkg_resources

###### Files ######
test_snv_vcf = "resources/demo/643594.clinical.vcf.gz"
empty_vcf = "resources/demo/empty.clinical.SV.vcf.gz"

###### Paths ######
test_snv_vcf_path =  pkg_resources.resource_filename("cgbeacon2", test_snv_vcf)
test_empty_vcf_path = pkg_resources.resource_filename("cgbeacon2", empty_vcf)
