from KifuAssembler.src.incorporator import to_GoGui_sgf


def test_ToGoGuiSgf_CorrectlyReturns():
    sample_LG_kifu = "(;FF[4]EV[connect6.DEFAULT.mc.2019.mar.1.7]PB[gzero_bot]PW[5466]SO[" \
                     "http://www.littlegolem.com];B[j10];W[j7k8];B[j12i11];W[j8i8];B[h12l8];W[k9k12];B[g13k13];W[" \
                     "f14h10];B[i13j13])"

    actual = to_GoGui_sgf(sample_LG_kifu)

    expected = "(;FF[4]CA[UTF-8]AP[GoGui:1.5.1];W[jm];W[kl];B[jh];B[ii];W[jl];W[il];B[hh];B[ll];W[kk];W[kh];B[gg];B[kg];W[ff];W[hj];B[ig];B[jg])"

    assert actual == expected
