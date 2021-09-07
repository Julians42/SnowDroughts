#!bin/sh
while true
do
for year in {1979..2020}
do
   scp u10m_${year}.nc public:/home/Kai-chi.Tseng/u10m/template
   ssh public mv /home/Kai-chi.Tseng/u10m/template /home/Kai-chi.Tseng/u10m/u10m_${year}.nc
done
done