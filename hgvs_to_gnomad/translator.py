import re
import yaml
import subprocess

class Common:
    snp_pattern_all = re.compile(r"NC_(\d+)\.\d+:g\.(\d+)([ATGC])>([ATGC])")
    del_pattern_all = re.compile(r"NC_(\d+)\.\d+:g\.(\d+)_*(\d*)del$")
    ins_pattern_all = re.compile(r"NC_(\d+)\.\d+:g\.(\d+)_*(\d*)ins([ATGC]+)$")
    dup_pattern_all = re.compile(r"NC_(\d+)\.\d+:g\.(\d+)_*(\d*)dup$")
    delins_pattern_all = re.compile(
        r"NC_(\d+)\.\d+:g\.(\d+)_*(\d*)delins([ATGC]+)$")
    re_dict = {
        "SNP": snp_pattern_all,
        "DEL": del_pattern_all,
        "INS": ins_pattern_all,
        "DUP": dup_pattern_all,
        "DELINS": delins_pattern_all
    }
    grch37_dict = {
        "1": "NC_000001.10",
        "2": "NC_000002.11",
        "3": "NC_000003.11",
        "4": "NC_000004.11",
        "5": "NC_000005.9",
        "6": "NC_000006.11",
        "7": "NC_000007.13",
        "8": "NC_000008.10",
        "9": "NC_000009.11",
        "10": "NC_000010.10",
        "11": "NC_000011.9",
        "12": "NC_000012.11",
        "13": "NC_000013.10",
        "14": "NC_000014.8",
        "15": "NC_000015.9",
        "16": "NC_000016.9",
        "17": "NC_000017.10",
        "18": "NC_000018.9",
        "19": "NC_000019.9",
        "20": "NC_000020.10",
        "21": "NC_000021.8",
        "22": "NC_000022.10",
        "X":  "NC_000023.10",
        "Y": "NC_000024.9"
    }

    @classmethod
    def rt_re_pattern(cls, var_type: str) -> re.compile:
        return cls.re_dict[var_type]

    @classmethod
    def rt_grch37_nc(cls, chrnum: str) -> str:
        return cls.grch37_dict[chrnum]


class HGVStoGNOMAD():
    def __init__(self):
        with open("config.yaml") as yml:
            config = yaml.load(yml, Loader=yaml.FullLoader)
        self.hg19 = config["HG19"]["FASTA"]
        self.samtools = config["TOOL"]["SAMTOOLS"]
        self.vts = ["SNP", "DEL", "DUP", "INS", "DELINS"]
        self.vtfs = [
            self.translate_to_gnomadid_snp,
            self.translate_to_gnomadid_del,
            self.translate_to_gnomadid_dup,
            self.translate_to_gnomadid_ins,
            self.translate_to_gnomadid_delins]

    def samtools_faidx(self, chrom: int, start: int, end: int) -> str:
        """ hg19 index를 이용해서 원하는 포지션의 정보를 출력 """
        cmd = f"{self.samtools} faidx {self.hg19} chr{chrom}:{start}-{end}"
        sub_result = subprocess.run(cmd, shell=True, capture_output=True, check=True)
        return sub_result.stdout.decode()

    def get_ref_sequence(self, chrn: str, start: str, end: str) -> str:
        hg19_result = self.samtools_faidx(chrn, start, end)
        hg19_ref = hg19_result.split('\n')[1].upper()
        return hg19_ref

    def translate_to_gnomadid_snp(self, nc_hgvs, matched=False):
        if not matched:
            pattern = Common.rt_re_pattern("SNP")
            matched = pattern.search(nc_hgvs)
        chrn = int(matched.group(1))
        position = int(matched.group(2))
        ref = matched.group(3)
        alt = matched.group(4)
        hg19_ref = self.get_ref_sequence(chrn, position, position)
        if hg19_ref != ref:
            assert False, f"{(chrn, position, ref, alt, hg19_ref)}"
        cont = [str(chrn), str(position), ref, alt]
        return "-".join(cont)

    def translate_to_gnomadid_del(self, nc_hgvs, matched=False):
        if not matched:
            pattern = Common.rt_re_pattern("DEL")
            matched = pattern.search(nc_hgvs)
        chrom = int(matched.group(1))
        start = int(matched.group(2))
        end = matched.group(3)
        if not end:
            end = start
        hg19_del = self.get_ref_sequence(chrom, start-1, end)
        cont = [str(chrom), str(start-1), hg19_del, hg19_del[0]]
        return "-".join(cont)

    def translate_to_gnomadid_ins(self, nc_hgvs, matched=False):
        if not matched:
            pattern = Common.rt_re_pattern("INS")
            matched = pattern.search(nc_hgvs)
        chrom = int(matched.group(1))
        start = int(matched.group(2))
        end = matched.group(3)
        alt = matched.group(4)
        if not end:
            end = start
        hg19_ins = self.get_ref_sequence(chrom, start, end)
        new_ref = hg19_ins[1]
        new_alt = alt + hg19_ins[1]
        new_pos = start + 1
        cont = [chrom, new_pos, new_ref, new_alt]
        return "-".join([str(v) for v in cont])

    def translate_to_gnomadid_dup(self, nc_hgvs, matched=False):
        if not matched:
            pattern = Common.rt_re_pattern("DUP")
            matched = pattern.search(nc_hgvs)
        chrom = int(matched.group(1))
        start = int(matched.group(2))
        end = matched.group(3)
        if not end:
            end = start
        hg19_dup = self.get_ref_sequence(chrom, start, end)
        new_ref = hg19_dup
        new_alt = hg19_dup * 2
        new_pos = start
        if len(hg19_dup) > 1:
            new_pos = start + len(hg19_dup) - 1
            new_ref = hg19_dup[-1]
            new_alt = hg19_dup[-1] + hg19_dup
        cont = [chrom, new_pos, new_ref, new_alt]
        return "-".join([str(v) for v in cont])

    def translate_to_gnomadid_delins(self, nc_hgvs, matched=False):
        if not matched:
            pattern = Common.rt_re_pattern("DELINS")
            matched = pattern.search(nc_hgvs)
        chrom = int(matched.group(1))
        start = int(matched.group(2))
        end = matched.group(3)
        seq = matched.group(4)
        if not end:
            end = start
        hg19_delins = self.get_ref_sequence(chrom, start, end)
        cont = [chrom, start, hg19_delins, seq]
        return "-".join([str(v) for v in cont])

    def id_converter(self, nc_hgvs):
        res = False
        for var_type, var_type_f in zip(self.vts, self.vtfs):
            pattern = Common.rt_re_pattern(var_type)
            matched = pattern.search(nc_hgvs)
            if matched:
                res = var_type_f(nc_hgvs, matched)
                break
        if not res:
            assert res, print(f"{nc_hgvs}", file=sys.stderr)
        return res

    @classmethod
    def parse_applied_evidence_code(cls, code_str: str) -> str:
        """
        return:
        PS4, PS4- Moderate, PS4-Supporting, PS4-Unmet
        """
        res_dic = {
            "PS4 [MET]": "PS4",
            "PS4-Moderate [MET]": "PS4-Moderate",
            "PS4-Supporting [MET]": "PS4-Supporting",
            "PS4 [Unmet]": "PS4-Unmet"
        }
        res = None
        splitteds = code_str.split(",")
        for splitted in splitteds:
            if not "PS4" in splitted:
                continue
            res = res_dic[splitted.strip(" ")]
            break
        return res

    @classmethod
    def get_hgvs(cls, vcep_dict: dict) -> str:
        """
        docstring here
            :param vcep_dict: dict
        """
        key1 = "#Variation"
        key2 = "HGVS Expressions"
        res = []
        try:
            res.append(vcep_dict[key1].split()[0])
        except IndexError:
            tmpid = [v.strip(" ") for v in vcep_dict[key2].split(",") if "NM_" in v]
            if len(tmpid) == 0:
                res.append('')
            else:
                res.append(tmpid[-1])
        hgvg_nc = [v.strip(" ") for v in vcep_dict[key2].split(",") if "NC_" in v]
        res.extend(hgvg_nc)
        return tuple(res)

    @classmethod
    def get_grch37(cls, hgvs_tup: tuple) -> tuple:
        """
        return (hgvs.nm, hgvs.nc(GRCh37))
        """
        res = []
        res.append(hgvs_tup[0])
        for nces in hgvs_tup[1:]:
            nc_version = nces.split(":")[0]
            nc_name = nc_version.split(".")[0]
            chrn = str(int(nc_name[3:]))
            if Common.rt_grch37_nc(chrn) != nc_version:
                continue
            res.append(nces)
            break
        return tuple(res)
