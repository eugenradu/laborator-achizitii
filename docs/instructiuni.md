### Initializare bd

Fără seed, numai user/pass pentru admin:
```
docker-compose exec app flask init-db --no-seed
```

### Logs
```
docker compose logs -f app
```

### Backup și restore baza de date
Backup (cu container și volum rulând):
```
docker-compose exec -T db pg_dump -U nume_utilizator_pg -d laborator_achizitii_db > backup_YYYMMDDHHMM.sql
```
Restore (pe bază de date goală):
```
cat backup_YYYYMMDDHHMM.sql | docker-compose exec -T db psql -U nume_utilizator_pg -d laborator_achizitii_db
```
