//
// Created by marscher on 4/3/17.
//

#ifndef PYEMMA_KMEANS_H
#define PYEMMA_KMEANS_H

#include "Clustering.h"

namespace py = pybind11;


template <typename dtype>
class KMeans : public ClusteringBase<dtype> {
public:
    using parent_t = ClusteringBase<dtype>;
    using np_array = py::array_t<dtype, py::array::c_style | py::array::forcecast>;
    KMeans(unsigned int k,
           const std::string& metric,
           size_t input_dimension,
           py::object& callback) : ClusteringBase<dtype>(metric, input_dimension), k(k), callback(callback) {}
    /**
     * performs kmeans clustering on the given data chunk, provided a list of centers.
     * @param np_chunk
     * @param py_centers
     * @return updated centers.
     */
    np_array cluster(const np_array&, const np_array&) const;

    /**
     * evaluate the quality of the centers
     *
     * @return
     */
    dtype costFunction(const np_array&, const np_array&) const;

    /**
     * kmeans++ initialisation
     * @param np_data
     * @param random_seed
     * @return
     */
    np_array initCentersKMpp(const np_array& np_data, unsigned int random_seed) const;


    /**
     * call back function to inform about progress
     * @param callback None or Python function.
     */
    void set_callback(const py::object& callback) { this->callback = callback; }
protected:
    unsigned int k;
    py::object callback;

};

#include "bits/kmeans_bits.h"

#endif //PYEMMA_KMEANS_H
