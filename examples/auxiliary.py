import numpy as np

from moe.optimal_learning.python.cpp_wrappers import log_likelihood_mcmc, knowledge_gradient_mcmc
from moe.optimal_learning.python import repeated_domain
from moe.optimal_learning.python.python_version import optimization

from qaliboo import finite_domain
from qaliboo import machine_learning_models

def compute_suggested_minimum(domain: finite_domain.FiniteDomain,
                              gp_loglikelihood: log_likelihood_mcmc.GaussianProcessLogLikelihoodMCMC,
                              py_sgd_params_ps: optimization.GradientDescentParameters) -> np.ndarray:
    
    eval_pts = domain.generate_uniform_random_points_in_domain(int(1e2)) # here you sample continuous
    #eval_pts = domain.sample_points_in_domain(sample_size=int(1e3), allow_previously_sampled=True) # here you sample discrete 
    
    eval_pts = np.reshape(
        np.append(eval_pts, (gp_loglikelihood.get_historical_data_copy()).points_sampled[:, :gp_loglikelihood.dim]),
        (eval_pts.shape[0] + gp_loglikelihood._num_sampled, gp_loglikelihood.dim))
    
    post_mean = knowledge_gradient_mcmc.PosteriorMeanMCMC(
        gp_loglikelihood.models
    )


    test = np.zeros(eval_pts.shape[0])
    for i, pt in enumerate(eval_pts):
        post_mean.set_current_point(pt.reshape((1, gp_loglikelihood.dim)))
        test[i] = -post_mean.compute_objective_function()
    initial_point = eval_pts[np.argmin(test)].reshape((1, gp_loglikelihood.dim))
    

    domain_repeated = repeated_domain.RepeatedDomain(num_repeats=1,
                                                     domain=domain)
    ps_mean_opt = optimization.GradientDescentOptimizer(domain_repeated,
                                                        post_mean,
                                                        py_sgd_params_ps)
    report_point = optimization.multistart_optimize(ps_mean_opt,
                                                    initial_point,
                                                    num_multistarts=1)[0]
    
    report_point = report_point.ravel()
    
    return report_point # initial_point.ravel()


def compute_suggested_minimum_ML(domain: finite_domain.FiniteDomain,
                              gp_loglikelihood: log_likelihood_mcmc.GaussianProcessLogLikelihoodMCMC,
                              py_sgd_params_ps: optimization.GradientDescentParameters,
                              ml_model: machine_learning_models.ML_model) -> np.ndarray:
    
    eval_pts = domain.generate_uniform_random_points_in_domain(int(1e2)) # here you sample continuous
    #eval_pts = domain.sample_points_in_domain(sample_size=int(1e3), allow_previously_sampled=True) # here you sample discrete 
    
    eval_pts = np.reshape(
        np.append(eval_pts, (gp_loglikelihood.get_historical_data_copy()).points_sampled[:, :gp_loglikelihood.dim]),
        (eval_pts.shape[0] + gp_loglikelihood._num_sampled, gp_loglikelihood.dim))
    
    post_mean = knowledge_gradient_mcmc.PosteriorMeanMCMC(
        gp_loglikelihood.models
    )


    test = np.zeros(eval_pts.shape[0])
    for i, pt in enumerate(eval_pts):
        post_mean.set_current_point(pt.reshape((1, gp_loglikelihood.dim)))
        test[i] = -post_mean.compute_objective_function()
    initial_point = eval_pts[np.argmin(test)].reshape((1, gp_loglikelihood.dim))
    

    domain_repeated = repeated_domain.RepeatedDomain(num_repeats=1,
                                                     domain=domain)
    ps_mean_opt = optimization.GradientDescentOptimizer(domain_repeated,
                                                        post_mean,
                                                        py_sgd_params_ps)
    report_point = optimization.multistart_optimize(ps_mean_opt,
                                                    initial_point,
                                                    num_multistarts=1)[0]
    
    report_point = report_point.ravel()
    
    return report_point # initial_point.ravel()
