import axiosClient from '../axios';


class GeoJsonhApi {

  async upload_update(endpoint: string, endpoint_method: string, selectedFile: File ): Promise<ResponseWrapper<object>> {

    const formData = new FormData();
    formData.append("file", selectedFile);

    const response = await axiosClient.request<ResponseWrapper<object>>({
      method: endpoint_method,
      url: `/geojson/${endpoint}`,
      data: formData,
      headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
      }
    });


    return response.data
  }


  async delete_roads(): Promise<void>{

    await axiosClient.request({
      method: 'DELETE',
      url: '/geojson/delete_all',
    });

    location.reload()
    localStorage.clear()

  }

  async get_roadstimestamp(): Promise<ResponseWrapper<GroupedRoadFeature[]>> {

    const response = await axiosClient.request<ResponseWrapper<GroupedRoadFeature[]>>({
      method: 'GET',
      url: '/geojson/roads_timestamps',
    });

    return response.data
  }

  async get_roads_with_date(params: string): Promise<ResponseWrapper<any | null>> {

    const response = await axiosClient.request<ResponseWrapper<any | null>>({
      method: 'GET',
      url: `/geojson/${params}`,
    });

    return response.data
  }

}

export const geoJsonApi = new GeoJsonhApi();
