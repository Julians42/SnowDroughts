#!bin/sh
while true
do
for year in {1979..2020}
do
if [ -f "/home/Kai-chi.Tseng/u10m/u10m_${year}.nc" ]; then
  # file exists! move it
  echo "file /home/Kai-chi.Tseng/u10m/u10m_${year}.nc exists. move it!"
  sleep 10
  mv /home/Kai-chi.Tseng/u10m/u10m_${year}.nc /archive/Kai-chi.Tseng/data/ERA5_50km/u10m/
else
  clear
  echo "File /home/Kai-chi.Tseng/u10m/u10m_${year}.nc doesn't exists."
fi
done
done