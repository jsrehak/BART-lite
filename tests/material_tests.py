from nose.tools import *
from material import _mat
import numpy as np

testData_loc = './tests/testData/materials/'

class TestFunctionality:
    # Tests to verify the material class functions are working
    # properly
    
    @classmethod
    def setup_class(cls):
        filename = testData_loc + 'test_mat.xml'
        NSfile = testData_loc + 'test_mat_nonsource.xml'
        noXsecFile = testData_loc + 'test_mat_no_xsec.xml'
        zeroXsecFile = testData_loc + 'test_mat_zero_xsec.xml'
        threeGFile = testData_loc + 'test_mat_3grps.xml'
        cls.testmat = _mat(filename, grps = 2)
        cls.testmatT = _mat(filename, grps = 2, tr_scatt=True)
        cls.testNSmat = _mat(NSfile, grps = 2)
        cls.testNXmat = _mat(noXsecFile, grps = 2)
        cls.testZXmat = _mat(zeroXsecFile, grps = 2)
        cls.test3gmat = _mat(threeGFile, grps = 3)

    # INITIALIZATION TESTS ===========================================
        
    def test_mat_gen_prop(self):
        """ Reading a file should save the correct values to class vars. """
        ok_(type(self.testmat.prop["nu"]) == float, "Nu should be a float")
        ok_(self.testmat.prop["nu"] == 2.3, "Nu should be the correct value")
        ok_(self.testmat.gen['id'] == 'test_mat', "Mat ID should have correct value")

    def test_mat_xsec(self):
        """ Reading a file should save the correct xsec values """
        ok_(type(self.testmat.xsec['sig_t']) == np.ndarray, "Cross-section should be a numpy array")
        ok_(np.all(self.testmat.xsec['sig_t'] == [200.0, 300.0]), "Cross-sections should have correct values")


    def test_mat_gconst(self):
        """ Reading a file should save the correct gconst values """
        ok_(type(self.testmat.gconst['chi']) == np.ndarray, "Group constant should be a numpy array")
        ok_(np.all(self.testmat.gconst['chi'] == [0.25, 0.75]), "Group constant should have the correct value")

    def test_mat_issource(self):
        """ Reading a file should generate the correct isSource value """
        ok_(self.testmat.isSource, "Fission material be marked as a source")
        ok_(not self.testNSmat.isSource, "Non source material should be marked as a non-source")

    def test_scattering_matrix(self):
        ok_(np.array_equal(self.testmat.xsec['sig_s'],
                           np.array([[40,10],[20,30]])))

    def test_scattering_matrix_transpose(self):
        ok_(np.array_equal(self.testmatT.xsec['sig_s'],
                           np.array([[40, 20],[10, 30]])))
        
    # DERIVED QUANTITIES =============================================

    
    def test_mat_calc_inv_sigt(self):
        """ Calculated inv_sigt should be correct or 0 if no sig_t or equals 0"""
        ok_(np.allclose(self.testmat.derived['inv_sig_t'],
                        np.array([0.005, 0.003333333])),
            "Inverse Sig_t should calculate the correct value")
        
        ok_(np.allclose(self.testZXmat.derived['inv_sig_t'],
                        np.array([0.0, 0.033333333])),
            "Inverse Sig_t should return 0 if sig_t = 0")

    def test_mat_calc_diff_coeff(self):
        """ Calculated diff coef should be correct or 0 if no sig_t or equals 0"""
        ok_(np.allclose(self.testmat.derived['diff_coef'],
                        np.array([0.0016666667, 0.0011111111])),
            "Diff Coef should calculate the correct val")
        
        ok_(np.allclose(self.testZXmat.derived['diff_coef'],
                        np.array([0.0, 0.011111111])),
            "Diffusion Coef should return 0 if sig_t = 0")

    def test_mat_calc_nu_sigf(self):
        """ Calculated nu_sigf should be correct value """
        ok_(np.allclose(self.testmat.derived['chi_nu_sig_f'],
                        np.array([[28.75, 34.5], [86.25, 103.5]])),
            "Chi_nu_sig_f should be the correct value")

    def test_mat_no_xsec_no_chi_nu_sig_f(self):
        """ A material with no cross-section should not have a sig f nu
        value """
        ok_('chi_nu_sig_f' not in self.testNXmat.derived)

    def test_mat_calc_ksi_ua(self):
        """ Calculated thermal eigenvalue should be correct """
        ok_(np.allclose(self.test3gmat.derived['ksi_ua'],
                           np.array([0.93103448, 0.06896552])))


    def test_aceleration_properties(self):
        """ Calculated aceleration properties should be correct """
        ok_(np.allclose(self.test3gmat.derived['sig_t_ua'], 206.8965464),
            "Sig_t_ua test3gmat, incorrect value")
        ok_(np.allclose(self.test3gmat.derived['diff_coef_ua'],
                                0.001628352426751656),
            "Diff_coef_ua, test_mat3, incorrect value")
        
    def test_sig_r_value(self):
        """ Calculated sig_r should be correct type and value """
        ok_(isinstance(self.testmat.get('sig_r'), np.ndarray),
            ".get('sig_r') should return an array")
        ok_(np.array_equal(self.testmat.get('sig_r'),
                           np.array([160.0, 270.0])),
            ".get('sig_r') should return the correct value")

    def test_sig_r_ua_value(self):
        """ Calculated sig_r_ua should be correct value """
        ok_(np.allclose(self.test3gmat.derived['sig_r_ua'], 148.27585677650282))
        
    ## TEST ERRORS ===================================================

    @raises(RuntimeError)
    def test_mat_nonint_g_thermal(self):
        """ A non integer value of g_thermal should return a runtime
        error"""
        filename = testData_loc + 'test_bad_g_thermal_float.xml'
        badmat = _mat(filename, grps = 2)
    
    @raises(RuntimeError)
    def test_mat_bad_g_thermal(self):
        """ A value of g_thermal greater than n_grps should return
        a runtime error """
        filename = testData_loc + 'test_bad_g_thermal.xml'
        badmat = _mat(filename, grps = 2)
    
    @raises(KeyError)
    def test_mat_nxsec_no_inv(self):
        """ A material with no cross-sections should not have an inverted
        cross-section value """
        self.testNXmat.derived['inv_sig_t']

    @raises(KeyError)
    def test_mat_nxsec_no_inv(self):
        """ A material with no cross-section should not have an inv.
        cross-section value """
        self.testNXmat.derived['diff_coef']
        
    @raises(KeyError)
    def test_mat_bad_structure(self):
        """ Specifying a group structure not in the material file should return
        a Key error """
        filename = testData_loc + 'test_mat.xml'
        badMat = _mat(filename, grps = 3)

    # ASSERTION ERRORS ===============================================
    
    @raises(AssertionError)
    def test_mat_bad_filename(self):
        """ Reading a bad filename should return an assertion error. """
        filename = testData_loc + 'badname.xml'
        badMat = _mat(filename, grps = 2)

    # RUNTIME ERRORS =================================================
    
    @raises(AssertionError)
    def test_no_id(self):
        """ Uploading a material with no id should return an assertion error. """
        filename = testData_loc + 'test_no_id.xml'
        badMat = _mat(filename, grps = 2)
        
    @raises(RuntimeError)
    def test_xsec_sizes(self):
        """ All cross section arrays should be the same size. """
        filename = testData_loc + 'test_bad_xsec.xml'
        badMat = _mat(filename, grps = 2)

    @raises(RuntimeError)
    def test_xsec_pos(self):
        """ Negative cross sections should return a Runtime Error """
        filename = testData_loc + 'test_neg_xsec.xml'
        badMat = _mat(filename, grps = 2)
