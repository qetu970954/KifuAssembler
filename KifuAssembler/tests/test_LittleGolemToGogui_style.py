from KifuAssembler.src.incorporator import to_GoGui_sgf, to_Pure_sgf


def test_ToGoGuiSgf_CorrectlyReturns():
    sample_LG_kifu = "(;FF[4]EV[connect6.DEFAULT.mc.2019.mar.1.7]PB[gzero_bot]PW[5466]SO[" \
                     "http://www.littlegolem.net];B[j10];W[j7k8];B[j12i11];W[j8i8];B[h12l8];W[k9k12];B[g13k13];W[" \
                     "f14h10];B[i13j13])"

    actual = to_GoGui_sgf(sample_LG_kifu)

    expected = "(;FF[4]CA[UTF-8]AP[GoGui:1.5.1];W[JM];W[KL];B[JH];B[II];W[JL];W[IL];B[HH];B[LL];W[KK];W[KH];B[GG];B[KG];W[FF];W[HJ];B[IG];B[JG])"

    assert actual == expected


def test_ToPureSgf_CorrectlyReturns():
    sample_LG_kifu = "(;FF[4]EV[connect6.DEFAULT.mc.2020.may.1.11]PB[u2b]PW[FancyBen]SO[" \
                     "http://www.littlegolem.com];B[j10];W[k11i11];B[j12l11];W[i12i10];B[h11i9];)"
    expected = ";B[JJ];W[KK];W[IK];B[JL];B[LK];W[IL];W[IJ];B[HK];B[II]"
    actual = to_Pure_sgf(sample_LG_kifu)
    assert actual == expected
