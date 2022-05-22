public class CashierServiceImpl implements CashierService {

  @Autowired
  CacheServiceImpl cacheService;

  public List<Cashier> getByStoreId(String id) throws CacheException {
    String query = "SELECT * FROM /Cashier WHERE storeId = '" + id + "';";
    return cacheService.execute(query);
  }
  
} 