<?php

namespace App\Entity;

use App\Repository\BrandRepository;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity(repositoryClass: BrandRepository::class)]
class Brand
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\Column(length: 255)]
    private ?string $brand_name = null;

    #[ORM\Column]
    private ?int $brand_favorites = null;

    #[ORM\Column]
    private ?int $item_count = null;

    #[ORM\Column(length: 255, nullable: true)]
    private ?string $vinted_slug = null;

    #[ORM\Column(length: 255, nullable: true)]
    private ?string $site_slug = null;

    public function getId(): ?int
    {
        return $this->id;
    }

    public function setId(int $id): static
    {
        $this->id = $id;

        return $this;
    }

    public function getBrandName(): ?string
    {
        return $this->brand_name;
    }

    public function setBrandName(string $brand_name): static
    {
        $this->brand_name = $brand_name;

        return $this;
    }

    public function getBrandFavorites(): ?int
    {
        return $this->brand_favorites;
    }

    public function setBrandFavorites(int $brand_favorites): static
    {
        $this->brand_favorites = $brand_favorites;

        return $this;
    }

    public function getItemCount(): ?int
    {
        return $this->item_count;
    }

    public function setItemCount(int $item_count): static
    {
        $this->item_count = $item_count;

        return $this;
    }

    public function getVintedSlug(): ?string
    {
        return $this->vinted_slug;
    }

    public function setVintedSlug(?string $vinted_slug): static
    {
        $this->vinted_slug = $vinted_slug;

        return $this;
    }

    public function getSiteSlug(): ?string
    {
        return $this->site_slug;
    }

    public function setSiteSlug(?string $site_slug): static
    {
        $this->site_slug = $site_slug;

        return $this;
    }
}
