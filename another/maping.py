import folium
from folium.plugins import AntPath

# 출발지와 목적지 좌표
start_coords = [37.5665, 126.9780]  # 서울 시청
end_coords = [37.5796, 126.9770]    # 경복궁

# 지도의 초기 위치를 출발지로 설정
map_ = folium.Map(location=start_coords, zoom_start=13)

# 출발지와 목적지에 마커 추가
folium.Marker(start_coords, tooltip='Start: 서울 시청').add_to(map_)
folium.Marker(end_coords, tooltip='End: 경복궁').add_to(map_)

# 출발지와 목적지 사이의 경로 추가
AntPath(locations=[start_coords, end_coords], color='blue', weight=5).add_to(map_)

# 지도를 HTML 파일로 저장
map_.save('map.html')