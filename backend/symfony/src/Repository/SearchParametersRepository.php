<?php

namespace App\Repository;

use App\Entity\SearchParameters;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Persistence\ManagerRegistry;

/**
 * @extends ServiceEntityRepository<SearchParameters>
 *
 * @method SearchParameters|null find($id, $lockMode = null, $lockVersion = null)
 * @method SearchParameters|null findOneBy(array $criteria, array $orderBy = null)
 * @method SearchParameters[]    findAll()
 * @method SearchParameters[]    findBy(array $criteria, array $orderBy = null, $limit = null, $offset = null)
 */
class SearchParametersRepository extends ServiceEntityRepository
{
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, SearchParameters::class);
    }

//    /**
//     * @return SearchParameters[] Returns an array of SearchParameters objects
//     */
//    public function findByExampleField($value): array
//    {
//        return $this->createQueryBuilder('s')
//            ->andWhere('s.exampleField = :val')
//            ->setParameter('val', $value)
//            ->orderBy('s.id', 'ASC')
//            ->setMaxResults(10)
//            ->getQuery()
//            ->getResult()
//        ;
//    }

//    public function findOneBySomeField($value): ?SearchParameters
//    {
//        return $this->createQueryBuilder('s')
//            ->andWhere('s.exampleField = :val')
//            ->setParameter('val', $value)
//            ->getQuery()
//            ->getOneOrNullResult()
//        ;
//    }
}
