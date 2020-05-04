import pkg_resources

###### Files ######
test_snv_vcf = "resources/demo/643594.clinical.vcf.gz"
test_sv_vcf = "resources/demo/643594.clinical.SV.vcf.gz"
empty_vcf = "resources/demo/empty.clinical.SV.vcf.gz"
panel1 = "resources/demo/panel1.bed"
panel2 = "resources/demo/panel2.bed"

###### Paths ######
test_snv_vcf_path = pkg_resources.resource_filename("cgbeacon2", test_snv_vcf)
test_sv_vcf_path = pkg_resources.resource_filename("cgbeacon2", test_sv_vcf)
test_empty_vcf_path = pkg_resources.resource_filename("cgbeacon2", empty_vcf)
panel1_path = pkg_resources.resource_filename("cgbeacon2", panel1)
panel2_path = pkg_resources.resource_filename("cgbeacon2", panel2)
